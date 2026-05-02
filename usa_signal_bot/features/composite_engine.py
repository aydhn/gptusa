from pathlib import Path
from typing import List, Dict, Optional
import datetime
from usa_signal_bot.features.composite_models import (
    FeatureGroupSpec, CompositeFeatureSet, FeatureGroupResult,
    CompositeFeatureResult, CompositeFeatureMetadata, feature_group_result_to_dict,
    composite_feature_result_to_dict, composite_feature_metadata_to_dict
)
from usa_signal_bot.core.enums import FeatureGroupType, FeatureComputationStatus, FeaturePipelineStatus, FeatureOutputPartition
from usa_signal_bot.features.engine import FeatureEngine, FeatureInput
from usa_signal_bot.features.feature_groups import create_default_feature_group_registry
from usa_signal_bot.core.exceptions import FeatureGroupError, CompositeFeatureError
from usa_signal_bot.features.input_contract import FeatureBatchInput
import json

class CompositeFeatureEngine:
    def __init__(self, feature_engine: FeatureEngine, data_root: Path):
        self.feature_engine = feature_engine
        self.data_root = data_root

    def compute_group_for_batch(self, batch: FeatureBatchInput, group_spec: FeatureGroupSpec, write_outputs: bool = False) -> FeatureGroupResult:
        if not group_spec.enabled:
            return FeatureGroupResult(
                group_name=group_spec.group_name,
                group_type=group_spec.group_type,
                status=FeatureComputationStatus.NOT_STARTED,
                produced_features=[],
                row_count=0,
                symbols_processed=[],
                timeframes_processed=[],
                storage_paths=[],
                warnings=[],
                errors=[]
            )

        try:
            if group_spec.group_type == FeatureGroupType.TREND:
                batch_result = self.feature_engine.compute_trend_set_for_batch(batch, set_name=group_spec.indicator_set_name)
            elif group_spec.group_type == FeatureGroupType.MOMENTUM:
                batch_result = self.feature_engine.compute_momentum_set_for_batch(batch, set_name=group_spec.indicator_set_name)
            elif group_spec.group_type == FeatureGroupType.VOLATILITY:
                batch_result = self.feature_engine.compute_volatility_set_for_batch(batch, set_name=group_spec.indicator_set_name)
            elif group_spec.group_type == FeatureGroupType.VOLUME:
                batch_result = self.feature_engine.compute_volume_set_for_batch(batch, set_name=group_spec.indicator_set_name)
            elif group_spec.group_type == FeatureGroupType.PRICE_ACTION:
                batch_result = self.feature_engine.compute_price_action_set_for_batch(batch, set_name=group_spec.indicator_set_name)
            elif group_spec.group_type == FeatureGroupType.DIVERGENCE:
                batch_result = self.feature_engine.compute_divergence_set_for_batch(batch, set_name=group_spec.indicator_set_name)
            elif group_spec.group_type == FeatureGroupType.BASIC:
                # Basic doesn't have a specific set method in the engine
                from usa_signal_bot.features.models import IndicatorSet
                ind_set = IndicatorSet(name=group_spec.indicator_set_name, indicators=["close_return", "close_sma_20"], params_by_indicator={})
                batch_result = self.feature_engine.compute_for_batch(batch, ind_set.indicators, ind_set.params_by_indicator)
            else:
                from usa_signal_bot.features.models import IndicatorSet
                ind_set = IndicatorSet(name=group_spec.indicator_set_name, indicators=[], params_by_indicator={})
                batch_result = self.feature_engine.compute_for_batch(batch, ind_set.indicators, ind_set.params_by_indicator)

            storage_paths = []
            if write_outputs and batch_result.is_successful():
                from usa_signal_bot.features.feature_store import write_group_feature_output
                path = write_group_feature_output(self.data_root, batch_result, group_name=group_spec.group_name)
                if path:
                    storage_paths.append(str(path))

            return FeatureGroupResult(
                group_name=group_spec.group_name,
                group_type=group_spec.group_type,
                status=batch_result.status,
                produced_features=batch_result.produced_features,
                row_count=len(batch_result.feature_rows),
                symbols_processed=batch_result.symbols_processed,
                timeframes_processed=batch_result.timeframes_processed,
                storage_paths=storage_paths,
                warnings=batch_result.warnings,
                errors=batch_result.errors
            )

        except Exception as e:
            return FeatureGroupResult(
                group_name=group_spec.group_name,
                group_type=group_spec.group_type,
                status=FeatureComputationStatus.FAILED,
                produced_features=[],
                row_count=0,
                symbols_processed=[],
                timeframes_processed=[],
                storage_paths=[],
                warnings=[],
                errors=[f"Exception computing group {group_spec.group_name}: {str(e)}"]
            )

    def compute_composite_for_batch(self, batch: FeatureBatchInput, composite_set: CompositeFeatureSet, write_outputs: bool = False, partition: FeatureOutputPartition = FeatureOutputPartition.BY_GROUP) -> CompositeFeatureResult:
        group_results: List[FeatureGroupResult] = []
        enabled_groups = [g for g in composite_set.groups if g.enabled]

        for group in enabled_groups:
            write_group = write_outputs and partition == FeatureOutputPartition.BY_GROUP
            group_res = self.compute_group_for_batch(batch, group, write_outputs=write_group)
            group_results.append(group_res)

        successful = [r for r in group_results if r.status == FeatureComputationStatus.COMPLETED]
        failed = [r for r in group_results if r.status == FeatureComputationStatus.FAILED]

        if not enabled_groups:
            status = FeaturePipelineStatus.FAILED
        elif len(successful) == len(enabled_groups):
            status = FeaturePipelineStatus.COMPLETED
        elif len(successful) > 0:
            status = FeaturePipelineStatus.PARTIAL_SUCCESS
        else:
            status = FeaturePipelineStatus.FAILED

        produced_features = set()
        total_rows = 0
        symbols_processed = set()
        timeframes_processed = set()
        warnings = []
        errors = []

        for r in group_results:
            produced_features.update(r.produced_features)
            total_rows = max(total_rows, r.row_count)
            symbols_processed.update(r.symbols_processed)
            timeframes_processed.update(r.timeframes_processed)
            warnings.extend(r.warnings)
            errors.extend(r.errors)

        produced_features_list = sorted(list(produced_features))

        output_paths = {}
        if write_outputs and partition == FeatureOutputPartition.BY_GROUP:
            for r in successful:
                if r.storage_paths:
                    output_paths[r.group_name] = r.storage_paths[0]

        return CompositeFeatureResult(
            composite_set_name=composite_set.name,
            status=status,
            group_results=group_results,
            total_rows=total_rows,
            total_features=len(produced_features_list),
            produced_features=produced_features_list,
            symbols_processed=sorted(list(symbols_processed)),
            timeframes_processed=sorted(list(timeframes_processed)),
            output_paths=output_paths,
            warnings=warnings,
            errors=errors,
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )

    def compute_composite_from_cache(self, symbols: List[str], timeframes: List[str], composite_set_name: str = "core", provider_name: str = "yfinance", write_outputs: bool = False, partition: FeatureOutputPartition = FeatureOutputPartition.BY_GROUP) -> CompositeFeatureResult:
        from usa_signal_bot.features.composite_sets import get_composite_feature_set
        from usa_signal_bot.data.cache import read_cached_bars_for_symbols_timeframe
        from usa_signal_bot.features.input_contract import FeatureInput, FeatureBatchInput

        cset = get_composite_feature_set(composite_set_name)

        inputs = []
        for sym in symbols:
            for tf in timeframes:
                bars = read_cached_bars_for_symbols_timeframe(self.data_root, [sym], tf, provider_name=provider_name)
                if bars:
                    inputs.append(FeatureInput(symbol=sym, timeframe=tf, bars=bars))

        import datetime
        batch = FeatureBatchInput(inputs=inputs, created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), provider_name=provider_name)
        return self.compute_composite_for_batch(batch, cset, write_outputs=write_outputs, partition=partition)


    def write_composite_metadata(self, result: CompositeFeatureResult, provider_name: str, universe_name: Optional[str] = None) -> CompositeFeatureMetadata:
        import uuid
        from usa_signal_bot.features.feature_store import write_composite_metadata_json

        metadata = CompositeFeatureMetadata(
            metadata_id=str(uuid.uuid4()),
            composite_set_name=result.composite_set_name,
            provider_name=provider_name,
            universe_name=universe_name,
            symbols=result.symbols_processed,
            timeframes=result.timeframes_processed,
            feature_groups=[r.group_name for r in result.group_results],
            produced_features=result.produced_features,
            total_rows=result.total_rows,
            total_features=result.total_features,
            created_at_utc=result.created_at_utc,
            storage_paths=list(result.output_paths.values()),
            validation_report_paths=[]
        )

        write_composite_metadata_json(self.data_root, metadata)
        return metadata

    def write_composite_result_json(self, result: CompositeFeatureResult) -> Path:
        from usa_signal_bot.features.feature_store import build_composite_output_dir

        output_dir = build_composite_output_dir(self.data_root, result.composite_set_name)
        file_path = output_dir / "composite_result.json"

        data = composite_feature_result_to_dict(result)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        return file_path
