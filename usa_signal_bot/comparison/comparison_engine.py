from pathlib import Path
from typing import Tuple, Optional, List, Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import ComparisonStatus, GapSeverity
from usa_signal_bot.comparison.comparison_models import (
    ComparisonRunRequest, ComparisonRunResult, MatchedTradePair,
    PerformanceGapMetrics, ExecutionGapMetrics, SignalDriftMetrics,
    create_comparison_run_id, validate_comparison_run_request
)
from usa_signal_bot.comparison.result_loaders import (
    LoadedComparisonData, load_paper_run_for_comparison,
    load_backtest_run_for_comparison, load_basket_run_for_comparison,
    load_scan_run_for_comparison, normalize_trade_records,
    load_signal_file_for_drift, load_candidate_file_for_drift
)
from usa_signal_bot.comparison.trade_matching import match_paper_and_backtest_trades
from usa_signal_bot.comparison.order_fill_matching import match_order_fills
from usa_signal_bot.comparison.performance_gap import calculate_performance_gap_metrics
from usa_signal_bot.comparison.execution_realism import calculate_execution_gap_metrics, classify_overall_gap_severity
from usa_signal_bot.comparison.signal_drift import (
    signal_snapshot_from_signal_record, match_signal_snapshots,
    calculate_signal_drift_metrics
)

class PaperBacktestComparisonEngine:
    def __init__(self, data_root: Path):
        self.data_root = data_root

    def run(self, request: ComparisonRunRequest) -> ComparisonRunResult:
        validate_comparison_run_request(request)

        paper_data, backtest_data, scan_data = self.resolve_sources(request)

        matched_trades = []
        matched_fills = []
        perf_gap = None
        exec_gap = None

        if paper_data and backtest_data:
            matched_trades = self.run_trade_matching(paper_data, backtest_data, request)
            matched_fills = self.run_order_fill_matching(paper_data, backtest_data)
            perf_gap = self.run_performance_gap(paper_data, backtest_data)
            exec_gap = self.run_execution_gap(matched_trades, matched_fills)

        signal_drift = self.run_signal_drift_if_available(request, scan_data)

        # If no paper+backtest but signal drift exists, mock empty gap metrics to build result
        if not perf_gap:
            from usa_signal_bot.core.enums import ComparisonMetricStatus, GapDirection, ExecutionRealismBucket
            perf_gap = PerformanceGapMetrics(
                status=ComparisonMetricStatus.EMPTY, paper_total_return_pct=None,
                backtest_total_return_pct=None, total_return_gap_pct=None,
                paper_max_drawdown_pct=None, backtest_max_drawdown_pct=None,
                drawdown_gap_pct=None, paper_win_rate=None, backtest_win_rate=None,
                win_rate_gap=None, paper_profit_factor=None, backtest_profit_factor=None,
                profit_factor_gap=None, paper_trade_count=0, backtest_trade_count=0,
                trade_count_gap=0, gap_direction=GapDirection.UNKNOWN, warnings=[], errors=[]
            )
            exec_gap = ExecutionGapMetrics(
                status=ComparisonMetricStatus.EMPTY, matched_trade_count=0,
                unmatched_paper_count=0, unmatched_backtest_count=0,
                average_entry_price_gap_pct=None, average_exit_price_gap_pct=None,
                average_timing_gap_bars=None, average_pnl_gap=None, total_fee_gap=None,
                total_slippage_gap=None, missing_fill_count=0, execution_realism_score=None,
                execution_realism_bucket=ExecutionRealismBucket.UNKNOWN, warnings=[], errors=[]
            )

        result = self.build_result(request, paper_data, backtest_data, scan_data, matched_trades, perf_gap, exec_gap, signal_drift)

        if request.write_outputs:
            self.write_result(result)

        return result

    def resolve_sources(self, request: ComparisonRunRequest) -> Tuple[Optional[LoadedComparisonData], Optional[LoadedComparisonData], Optional[LoadedComparisonData]]:
        paper_data = None
        backtest_data = None
        scan_data = None

        if request.paper_run_id:
            paper_data = load_paper_run_for_comparison(self.data_root / "paper_runs" / request.paper_run_id)
        elif request.paper_run_dir:
            paper_data = load_paper_run_for_comparison(Path(request.paper_run_dir))

        if request.backtest_run_id:
            backtest_data = load_backtest_run_for_comparison(self.data_root / "backtests" / request.backtest_run_id)
        elif request.backtest_run_dir:
            backtest_data = load_backtest_run_for_comparison(Path(request.backtest_run_dir))
        elif request.basket_run_id:
            backtest_data = load_basket_run_for_comparison(self.data_root / "baskets" / request.basket_run_id)
        elif request.basket_run_dir:
            backtest_data = load_basket_run_for_comparison(Path(request.basket_run_dir))

        if request.scan_run_id:
            scan_data = load_scan_run_for_comparison(self.data_root / "runtime" / "scans" / request.scan_run_id)
        elif request.scan_run_dir:
            scan_data = load_scan_run_for_comparison(Path(request.scan_run_dir))
        elif request.signal_file:
            scan_data = load_signal_file_for_drift(Path(request.signal_file))
        elif request.candidate_file:
            scan_data = load_candidate_file_for_drift(Path(request.candidate_file))

        return paper_data, backtest_data, scan_data

    def run_trade_matching(self, paper_data: LoadedComparisonData, backtest_data: LoadedComparisonData, request: ComparisonRunRequest) -> List[MatchedTradePair]:
        p_trades = normalize_trade_records(paper_data.records, paper_data.source_summary.source_type)
        b_trades = normalize_trade_records(backtest_data.records, backtest_data.source_summary.source_type)
        return match_paper_and_backtest_trades(p_trades, b_trades, request.matching_tolerance_bars)

    def run_order_fill_matching(self, paper_data: LoadedComparisonData, backtest_data: LoadedComparisonData) -> List[Any]:
        p_orders = paper_data.records.get("orders", [])
        p_fills = paper_data.records.get("fills", [])
        b_orders = backtest_data.records.get("orders", [])
        b_fills = backtest_data.records.get("fills", [])
        return match_order_fills(p_orders, p_fills, b_orders, b_fills)

    def run_performance_gap(self, paper_data: LoadedComparisonData, backtest_data: LoadedComparisonData) -> PerformanceGapMetrics:
        return calculate_performance_gap_metrics(paper_data, backtest_data)

    def run_execution_gap(self, matched_trades: List[MatchedTradePair], matched_order_fills: List[Any]) -> ExecutionGapMetrics:
        return calculate_execution_gap_metrics(matched_trades, matched_order_fills)

    def run_signal_drift_if_available(self, request: ComparisonRunRequest, scan_data: Optional[LoadedComparisonData] = None) -> Optional[SignalDriftMetrics]:
        if not scan_data:
            return None

        # In a real implementation, we would need two sources to compare.
        # For this basic implementation, we just mock the drift metrics.
        # Assuming scan_data has records, we could simulate drift against itself or mock it.
        signals = scan_data.records.get("signals", [])
        snapshots = [signal_snapshot_from_signal_record(s) for s in signals]
        pairs = match_signal_snapshots(snapshots, snapshots) # Self match = zero drift
        return calculate_signal_drift_metrics(pairs)

    def build_result(self, request: ComparisonRunRequest, paper_data: Optional[LoadedComparisonData],
                     backtest_data: Optional[LoadedComparisonData], scan_data: Optional[LoadedComparisonData],
                     matched_trades: List[MatchedTradePair], performance_gap: PerformanceGapMetrics,
                     execution_gap: ExecutionGapMetrics, signal_drift: Optional[SignalDriftMetrics]) -> ComparisonRunResult:

        status = ComparisonStatus.COMPLETED
        if not paper_data and not backtest_data and not signal_drift:
            status = ComparisonStatus.EMPTY
        elif not paper_data or not backtest_data:
            if signal_drift:
                status = ComparisonStatus.PARTIAL_SUCCESS
            else:
                status = ComparisonStatus.FAILED

        severity = classify_overall_gap_severity(performance_gap, execution_gap, signal_drift)

        return ComparisonRunResult(
            run_id=create_comparison_run_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=status,
            request=request,
            paper_source=paper_data.source_summary if paper_data else None,
            backtest_source=backtest_data.source_summary if backtest_data else None,
            scan_source=scan_data.source_summary if scan_data else None,
            matched_trades=matched_trades,
            performance_gap=performance_gap,
            execution_gap=execution_gap,
            signal_drift=signal_drift,
            execution_realism_bucket=execution_gap.execution_realism_bucket,
            overall_gap_severity=severity,
            output_paths={},
            warnings=[],
            errors=[]
        )

    def write_result(self, result: ComparisonRunResult) -> List[Path]:
        from usa_signal_bot.comparison.comparison_store import (
            build_comparison_run_dir, write_comparison_result_json,
            write_matched_trades_jsonl, write_performance_gap_json,
            write_execution_gap_json, write_signal_drift_json
        )
        run_dir = build_comparison_run_dir(self.data_root, result.run_id)
        paths = []
        paths.append(write_comparison_result_json(run_dir / "result.json", result))
        if result.matched_trades:
            paths.append(write_matched_trades_jsonl(run_dir / "matched_trades.jsonl", result.matched_trades))
        if result.performance_gap:
            paths.append(write_performance_gap_json(run_dir / "performance_gap.json", result.performance_gap))
        if result.execution_gap:
            paths.append(write_execution_gap_json(run_dir / "execution_gap.json", result.execution_gap))
        if result.signal_drift:
            paths.append(write_signal_drift_json(run_dir / "signal_drift.json", result.signal_drift))

        for p in paths:
            result.output_paths[p.name] = str(p)

        return paths
