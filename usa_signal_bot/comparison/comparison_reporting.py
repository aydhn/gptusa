from pathlib import Path
from typing import Optional, List

from usa_signal_bot.comparison.comparison_models import (
    ComparisonSourceSummary, MatchedTradePair, PerformanceGapMetrics,
    ExecutionGapMetrics, SignalDriftMetrics, ComparisonRunResult
)
from usa_signal_bot.comparison.comparison_validation import ComparisonValidationReport

def comparison_source_summary_to_text(summary: Optional[ComparisonSourceSummary]) -> str:
    if not summary:
        return "Source: None"
    return f"Source [{summary.source_type.value}]: {summary.record_count} records from {summary.source_id}"

def matched_trade_pair_to_text(pair: MatchedTradePair) -> str:
    return f"[{pair.match_status.value}] {pair.symbol} {pair.timeframe} - Pnl Gap: {pair.pnl_gap if pair.pnl_gap else 'N/A'}"

def matched_trades_report_to_text(pairs: List[MatchedTradePair], limit: int = 30) -> str:
    from usa_signal_bot.comparison.trade_matching import matched_trades_to_text
    return matched_trades_to_text(pairs, limit)

def performance_gap_report_to_text(metrics: PerformanceGapMetrics) -> str:
    from usa_signal_bot.comparison.performance_gap import performance_gap_metrics_to_text
    return performance_gap_metrics_to_text(metrics)

def execution_gap_report_to_text(metrics: ExecutionGapMetrics) -> str:
    from usa_signal_bot.comparison.execution_realism import execution_gap_metrics_to_text
    return execution_gap_metrics_to_text(metrics)

def signal_drift_report_to_text(metrics: Optional[SignalDriftMetrics]) -> str:
    if not metrics:
        return "Signal Drift: Not Available"
    from usa_signal_bot.comparison.signal_drift import signal_drift_metrics_to_text
    return signal_drift_metrics_to_text(metrics)

def comparison_run_result_to_text(result: ComparisonRunResult, limit: int = 30) -> str:
    lines = [
        "========================================",
        "PAPER VS BACKTEST COMPARISON REPORT",
        "========================================",
        f"Run ID: {result.run_id}",
        f"Status: {result.status.value}",
        f"Severity: {result.overall_gap_severity.value}",
        "",
        comparison_source_summary_to_text(result.paper_source),
        comparison_source_summary_to_text(result.backtest_source),
        "",
        performance_gap_report_to_text(result.performance_gap),
        "",
        execution_gap_report_to_text(result.execution_gap),
        ""
    ]
    if result.signal_drift:
        lines.append(signal_drift_report_to_text(result.signal_drift))
        lines.append("")

    lines.append(comparison_limitations_text())
    return "\n".join(lines)

def comparison_limitations_text() -> str:
    return (
        "LIMITATIONS & DISCLAIMER:\n"
        "- Paper and backtest are both simulations.\n"
        "- Real broker execution, slippage, and latency may differ significantly.\n"
        "- This comparison is NOT investment advice and does NOT guarantee future performance.\n"
        "- No live orders or demo orders are executed by this system."
    )

def write_comparison_report_json(path: Path, result: ComparisonRunResult, validation_report: Optional[ComparisonValidationReport] = None) -> Path:
    from usa_signal_bot.comparison.comparison_store import write_comparison_result_json
    return write_comparison_result_json(path, result)
