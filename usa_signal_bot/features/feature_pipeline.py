from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from pathlib import Path
import datetime
import json
import logging
from usa_signal_bot.features.composite_engine import CompositeFeatureEngine
from usa_signal_bot.features.composite_models import CompositeFeatureResult, CompositeFeatureMetadata
from usa_signal_bot.core.enums import FeaturePipelineStatus, FeatureOutputPartition
from usa_signal_bot.core.exceptions import FeaturePipelineError, FeatureInputError

logger = logging.getLogger(__name__)

@dataclass
class FeaturePipelineRequest:
    composite_set_name: str = "core"
    provider_name: str = "yfinance"
    symbols: Optional[List[str]] = None
    timeframes: Optional[List[str]] = None
    use_latest_eligible_symbols: bool = True
    universe_name: Optional[str] = None
    write_outputs: bool = True
    partition: FeatureOutputPartition = FeatureOutputPartition.BY_GROUP
    max_symbols: Optional[int] = None

@dataclass
class FeaturePipelineResult:
    request: FeaturePipelineRequest
    status: FeaturePipelineStatus
    composite_result: CompositeFeatureResult
    metadata: Optional[CompositeFeatureMetadata]
    eligible_symbols_used: List[str]
    missing_cache_symbols: List[str]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]
    created_at_utc: str

class FeaturePipeline:
    def __init__(self, composite_engine: CompositeFeatureEngine, data_root: Path):
        self.composite_engine = composite_engine
        self.data_root = data_root

    def load_latest_eligible_symbols(self, data_root: Path) -> List[str]:
        try:
            from usa_signal_bot.universe.readiness_gate import load_latest_universe_readiness_report
            report = load_latest_universe_readiness_report(data_root)
            if report and hasattr(report, "eligible_symbols"):
                return list(report.eligible_symbols)
            return []
        except Exception as e:
            logger.warning(f"Could not load latest eligible symbols: {e}")
            return []

    def resolve_symbols(self, request: FeaturePipelineRequest) -> List[str]:
        if request.symbols is not None and len(request.symbols) > 0:
            symbols = request.symbols
        elif request.use_latest_eligible_symbols:
            symbols = self.load_latest_eligible_symbols(self.data_root)
            if not symbols:
                from usa_signal_bot.universe.active import resolve_active_universe_symbols
                try:
                    symbols = resolve_active_universe_symbols(self.data_root)
                except Exception:
                    symbols = []
        else:
            symbols = []

        if not symbols:
            raise FeatureInputError("No symbols resolved for feature pipeline")

        if request.max_symbols and request.max_symbols > 0:
            return symbols[:request.max_symbols]
        return symbols

    def resolve_timeframes(self, request: FeaturePipelineRequest) -> List[str]:
        if request.timeframes and len(request.timeframes) > 0:
            return request.timeframes
        return ["1d"]

    def validate_cache_availability(self, symbols: List[str], timeframes: List[str], provider_name: str) -> Tuple[List[str], List[str]]:
        from usa_signal_bot.data.cache import read_cached_bars_for_symbols_timeframe

        available = []
        missing = []

        for sym in symbols:
            sym_has_all_data = True
            for tf in timeframes:
                bars = read_cached_bars_for_symbols_timeframe(self.data_root, [sym], tf, provider_name=provider_name)
                if not bars:
                    sym_has_all_data = False
                    break

            if sym_has_all_data:
                available.append(sym)
            else:
                missing.append(sym)

        return available, missing

    def run(self, request: FeaturePipelineRequest) -> FeaturePipelineResult:
        warnings = []
        errors = []

        try:
            symbols_to_process = self.resolve_symbols(request)
        except FeatureInputError as e:
            return FeaturePipelineResult(
                request=request,
                status=FeaturePipelineStatus.FAILED,
                composite_result=self._empty_composite_result(request.composite_set_name),
                metadata=None,
                eligible_symbols_used=[],
                missing_cache_symbols=[],
                output_paths={},
                warnings=[],
                errors=[str(e)],
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )

        timeframes = self.resolve_timeframes(request)

        available_symbols, missing_symbols = self.validate_cache_availability(
            symbols_to_process, timeframes, request.provider_name
        )

        if missing_symbols:
            warnings.append(f"{len(missing_symbols)} symbols missing cache data: {', '.join(missing_symbols[:5])}{'...' if len(missing_symbols) > 5 else ''}")

        if not available_symbols:
            errors.append("No symbols have available cache data")
            return FeaturePipelineResult(
                request=request,
                status=FeaturePipelineStatus.FAILED,
                composite_result=self._empty_composite_result(request.composite_set_name),
                metadata=None,
                eligible_symbols_used=symbols_to_process,
                missing_cache_symbols=missing_symbols,
                output_paths={},
                warnings=warnings,
                errors=errors,
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )

        try:
            composite_result = self.composite_engine.compute_composite_from_cache(
                symbols=available_symbols,
                timeframes=timeframes,
                composite_set_name=request.composite_set_name,
                provider_name=request.provider_name,
                write_outputs=request.write_outputs,
                partition=request.partition
            )

            metadata = None
            if request.write_outputs and composite_result.is_successful():
                metadata = self.composite_engine.write_composite_metadata(
                    composite_result,
                    request.provider_name,
                    request.universe_name
                )

            status = composite_result.status

            pipeline_result = FeaturePipelineResult(
                request=request,
                status=status,
                composite_result=composite_result,
                metadata=metadata,
                eligible_symbols_used=symbols_to_process,
                missing_cache_symbols=missing_symbols,
                output_paths=composite_result.output_paths,
                warnings=warnings + composite_result.warnings,
                errors=errors + composite_result.errors,
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )

            if request.write_outputs:
                self.write_pipeline_result_json(pipeline_result)

            return pipeline_result

        except Exception as e:
            errors.append(f"Pipeline execution failed: {str(e)}")
            return FeaturePipelineResult(
                request=request,
                status=FeaturePipelineStatus.FAILED,
                composite_result=self._empty_composite_result(request.composite_set_name),
                metadata=None,
                eligible_symbols_used=symbols_to_process,
                missing_cache_symbols=missing_symbols,
                output_paths={},
                warnings=warnings,
                errors=errors,
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )

    def write_pipeline_result_json(self, result: FeaturePipelineResult) -> Path:
        from usa_signal_bot.features.feature_store import build_composite_output_dir

        output_dir = build_composite_output_dir(self.data_root, result.request.composite_set_name)
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_path = output_dir / f"pipeline_result_{ts}.json"

        data = {
            "composite_set_name": result.request.composite_set_name,
            "status": result.status.value,
            "symbols_requested": len(result.eligible_symbols_used),
            "symbols_missing_cache": len(result.missing_cache_symbols),
            "total_features_produced": result.composite_result.total_features,
            "output_paths": result.output_paths,
            "errors": result.errors,
            "warnings": result.warnings,
            "created_at_utc": result.created_at_utc
        }

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        return file_path

    def _empty_composite_result(self, composite_set_name: str) -> CompositeFeatureResult:
        return CompositeFeatureResult(
            composite_set_name=composite_set_name,
            status=FeaturePipelineStatus.NOT_STARTED,
            group_results=[],
            total_rows=0,
            total_features=0,
            produced_features=[],
            symbols_processed=[],
            timeframes_processed=[],
            output_paths={},
            warnings=[],
            errors=["Pipeline failed before composite generation"],
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )
