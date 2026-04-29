from pathlib import Path
from typing import Optional, Tuple
import datetime
import logging
import uuid

from ..core.enums import PipelineRunStatus
from .models import MarketDataRequest, OHLCVBar
from .downloader import MarketDataDownloader
from .multitimeframe import (
    MultiTimeframeDataRequest, MultiTimeframeDataResult,
    TimeframeDownloadResult
)
from .coverage import DataCoverageReport, calculate_coverage_report
from .readiness import DataReadinessReport, DataReadinessCriteria, evaluate_readiness_from_coverage
from .cache import read_cached_bars_for_symbols_timeframe
from ..universe.loader import UniverseDefinition

logger = logging.getLogger(__name__)

class MultiTimeframeDataPipeline:
    def __init__(self, downloader: MarketDataDownloader, data_root: Path, provider_name: str = "yfinance"):
        self.downloader = downloader
        self.data_root = data_root
        self.provider_name = provider_name

    def run(self, request: MultiTimeframeDataRequest, write_reports: bool = True, readiness_criteria: Optional[DataReadinessCriteria] = None) -> Tuple[MultiTimeframeDataResult, DataCoverageReport, DataReadinessReport]:

        result = MultiTimeframeDataResult(
            request=request,
            status=PipelineRunStatus.RUNNING,
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )

        bars_by_timeframe = {}

        for spec in request.timeframe_specs:
            if not spec.enabled:
                continue

            tf_res = TimeframeDownloadResult(
                timeframe=spec.timeframe,
                symbols_requested=request.symbols
            )

            try:
                # We use the downloader's refresh logic
                req = MarketDataRequest(
                    symbols=request.symbols,
                    timeframe=spec.timeframe,
                    start_date=spec.start_date,
                    end_date=spec.end_date,
                    provider_name=self.provider_name,
                    adjusted=request.adjusted,
                    use_cache=request.use_cache
                )

                resp = self.downloader.download_with_refresh_decision(
                    req,
                    force_refresh=request.force_refresh,
                    use_cache=request.use_cache
                )

                tf_res.success = resp.success
                tf_res.response_bar_count = resp.bar_count()
                tf_res.symbols_returned = resp.symbols_returned()
                tf_res.errors.extend(resp.errors)
                tf_res.warnings.extend(resp.warnings)

                if resp.success:
                    bars_by_timeframe[spec.timeframe] = resp.bars
                else:
                    bars_by_timeframe[spec.timeframe] = []

            except Exception as e:
                tf_res.success = False
                tf_res.errors.append(str(e))
                bars_by_timeframe[spec.timeframe] = []

            result.results.append(tf_res)
            result.total_bars += tf_res.response_bar_count

        # Evaluate overall status
        successful_tfs = result.successful_timeframes()
        failed_tfs = result.failed_timeframes()

        if not failed_tfs:
            result.status = PipelineRunStatus.COMPLETED
        elif successful_tfs:
            result.status = PipelineRunStatus.PARTIAL_SUCCESS
        else:
            result.status = PipelineRunStatus.FAILED

        # Calculate coverage
        tfs = [s.timeframe for s in request.timeframe_specs if s.enabled]
        coverage = calculate_coverage_report(self.provider_name, request.symbols, tfs, bars_by_timeframe)

        # Calculate readiness
        readiness = evaluate_readiness_from_coverage(coverage, readiness_criteria)

        if write_reports:
            self.write_pipeline_reports(result, coverage, readiness)

        return result, coverage, readiness

    def run_for_symbols(self, symbols: list[str], timeframes: list[str], limit: Optional[int] = None, force_refresh: bool = False, readiness_criteria: Optional[DataReadinessCriteria] = None) -> Tuple[MultiTimeframeDataResult, DataCoverageReport, DataReadinessReport]:
        from .multitimeframe import build_timeframe_specs_from_list

        if limit and limit > 0:
            symbols = symbols[:limit]

        specs = build_timeframe_specs_from_list(timeframes)

        req = MultiTimeframeDataRequest(
            symbols=symbols,
            provider_name=self.provider_name,
            timeframe_specs=specs,
            force_refresh=force_refresh
        )

        return self.run(req, readiness_criteria=readiness_criteria)

    def run_for_universe(self, universe: UniverseDefinition, timeframes: list[str], limit: Optional[int] = None, asset_type: Optional[str] = None, force_refresh: bool = False, readiness_criteria: Optional[DataReadinessCriteria] = None) -> Tuple[MultiTimeframeDataResult, DataCoverageReport, DataReadinessReport]:

        symbols = []
        for row in universe.rows:
            if asset_type and row.asset_type.value != asset_type.upper():
                continue
            if row.is_active:
                symbols.append(row.symbol)

        return self.run_for_symbols(symbols, timeframes, limit=limit, force_refresh=force_refresh, readiness_criteria=readiness_criteria)

    def collect_cached_bars_for_timeframes(self, symbols: list[str], timeframes: list[str]) -> dict[str, list[OHLCVBar]]:
        res = {}
        for tf in timeframes:
            res[tf] = read_cached_bars_for_symbols_timeframe(self.data_root, symbols, tf, self.provider_name)
        return res

    def write_pipeline_reports(self, result: MultiTimeframeDataResult, coverage: DataCoverageReport, readiness: DataReadinessReport) -> list[Path]:
        from .coverage import write_coverage_report_json
        from .readiness import write_readiness_report_json
        from ..core.serialization import dataclass_to_dict
        import json

        reports_dir = self.data_root / "reports" / "data_readiness"
        reports_dir.mkdir(parents=True, exist_ok=True)

        run_id = str(uuid.uuid4())[:8]

        paths = []

        # Result
        res_path = reports_dir / f"mtf_result_{run_id}.json"
        with open(res_path, "w") as f:
            json.dump(dataclass_to_dict(result), f, indent=2)
        paths.append(res_path)

        # Coverage
        cov_path = reports_dir / f"coverage_{run_id}.json"
        write_coverage_report_json(cov_path, coverage)
        paths.append(cov_path)

        # Readiness
        read_path = reports_dir / f"readiness_{run_id}.json"
        write_readiness_report_json(read_path, readiness)
        paths.append(read_path)

        return paths
