from typing import Any, Dict, Optional, Union

from usa_signal_bot.core.enums import ComparisonMetricStatus, GapDirection, GapSeverity, ComparisonSourceType
from usa_signal_bot.comparison.comparison_models import PerformanceGapMetrics
from usa_signal_bot.comparison.result_loaders import LoadedComparisonData

def calculate_performance_gap_metrics(paper_data: Union[LoadedComparisonData, Dict[str, Any]], backtest_data: Union[LoadedComparisonData, Dict[str, Any]]) -> PerformanceGapMetrics:
    p_return = extract_total_return_pct(paper_data, ComparisonSourceType.PAPER_RUN)
    b_return = extract_total_return_pct(backtest_data, ComparisonSourceType.BACKTEST_RUN)

    p_dd = extract_max_drawdown_pct(paper_data, ComparisonSourceType.PAPER_RUN)
    b_dd = extract_max_drawdown_pct(backtest_data, ComparisonSourceType.BACKTEST_RUN)

    p_win = extract_win_rate(paper_data, ComparisonSourceType.PAPER_RUN)
    b_win = extract_win_rate(backtest_data, ComparisonSourceType.BACKTEST_RUN)

    p_pf = extract_profit_factor(paper_data, ComparisonSourceType.PAPER_RUN)
    b_pf = extract_profit_factor(backtest_data, ComparisonSourceType.BACKTEST_RUN)

    p_trades = extract_trade_count(paper_data, ComparisonSourceType.PAPER_RUN)
    b_trades = extract_trade_count(backtest_data, ComparisonSourceType.BACKTEST_RUN)

    return PerformanceGapMetrics(
        status=ComparisonMetricStatus.OK if (p_return is not None and b_return is not None) else ComparisonMetricStatus.INSUFFICIENT_DATA,
        paper_total_return_pct=p_return,
        backtest_total_return_pct=b_return,
        total_return_gap_pct=(p_return - b_return) if (p_return is not None and b_return is not None) else None,
        paper_max_drawdown_pct=p_dd,
        backtest_max_drawdown_pct=b_dd,
        drawdown_gap_pct=(p_dd - b_dd) if (p_dd is not None and b_dd is not None) else None,
        paper_win_rate=p_win,
        backtest_win_rate=b_win,
        win_rate_gap=(p_win - b_win) if (p_win is not None and b_win is not None) else None,
        paper_profit_factor=p_pf,
        backtest_profit_factor=b_pf,
        profit_factor_gap=(p_pf - b_pf) if (p_pf is not None and b_pf is not None) else None,
        paper_trade_count=p_trades,
        backtest_trade_count=b_trades,
        trade_count_gap=p_trades - b_trades,
        gap_direction=calculate_gap_direction(p_return, b_return, True),
        warnings=[],
        errors=[]
    )

def _get_records(data: Union[LoadedComparisonData, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(data, LoadedComparisonData):
        return data.records
    return data

def extract_total_return_pct(data: Union[LoadedComparisonData, Dict[str, Any]], source_type: Optional[ComparisonSourceType] = None) -> Optional[float]:
    records = _get_records(data)
    perf = records.get("performance", {})
    if not perf:
        # Fallback to analytics
        perf = records.get("analytics", {})

    return perf.get("total_return_pct", perf.get("total_return", perf.get("return_pct")))

def extract_max_drawdown_pct(data: Union[LoadedComparisonData, Dict[str, Any]], source_type: Optional[ComparisonSourceType] = None) -> Optional[float]:
    records = _get_records(data)
    perf = records.get("performance", {})
    if not perf:
        perf = records.get("analytics", {})
    return perf.get("max_drawdown_pct", perf.get("max_drawdown"))

def extract_win_rate(data: Union[LoadedComparisonData, Dict[str, Any]], source_type: Optional[ComparisonSourceType] = None) -> Optional[float]:
    records = _get_records(data)
    perf = records.get("performance", {})
    if not perf:
        perf = records.get("analytics", {})
    return perf.get("win_rate", perf.get("win_rate_pct", 0.0) / 100.0)

def extract_profit_factor(data: Union[LoadedComparisonData, Dict[str, Any]], source_type: Optional[ComparisonSourceType] = None) -> Optional[float]:
    records = _get_records(data)
    perf = records.get("performance", {})
    if not perf:
        perf = records.get("analytics", {})
    return perf.get("profit_factor")

def extract_trade_count(data: Union[LoadedComparisonData, Dict[str, Any]], source_type: Optional[ComparisonSourceType] = None) -> int:
    records = _get_records(data)
    trades = records.get("trades", [])
    if trades:
        return len(trades)
    perf = records.get("performance", {})
    if not perf:
        perf = records.get("analytics", {})
    return perf.get("total_trades", perf.get("trade_count", 0))

def calculate_gap_direction(paper_value: Optional[float], backtest_value: Optional[float], higher_is_better: bool = True) -> GapDirection:
    if paper_value is None or backtest_value is None:
        return GapDirection.UNKNOWN

    if paper_value > backtest_value:
        return GapDirection.PAPER_BETTER if higher_is_better else GapDirection.BACKTEST_BETTER
    elif paper_value < backtest_value:
        return GapDirection.BACKTEST_BETTER if higher_is_better else GapDirection.PAPER_BETTER
    else:
        return GapDirection.NEUTRAL

def classify_performance_gap_severity(metrics: PerformanceGapMetrics) -> GapSeverity:
    if metrics.status == ComparisonMetricStatus.INSUFFICIENT_DATA:
        return GapSeverity.UNKNOWN

    # Example simple threshold logic
    if metrics.total_return_gap_pct is not None and abs(metrics.total_return_gap_pct) > 10.0:
        return GapSeverity.CRITICAL
    if metrics.total_return_gap_pct is not None and abs(metrics.total_return_gap_pct) > 5.0:
        return GapSeverity.HIGH
    if metrics.drawdown_gap_pct is not None and abs(metrics.drawdown_gap_pct) > 5.0:
        return GapSeverity.MODERATE

    return GapSeverity.LOW

def performance_gap_metrics_to_text(metrics: PerformanceGapMetrics) -> str:
    lines = ["Performance Gap Metrics:"]
    lines.append(f"  Return Gap: {metrics.total_return_gap_pct:.2f}%" if metrics.total_return_gap_pct is not None else "  Return Gap: N/A")
    lines.append(f"  Drawdown Gap: {metrics.drawdown_gap_pct:.2f}%" if metrics.drawdown_gap_pct is not None else "  Drawdown Gap: N/A")
    lines.append(f"  Win Rate Gap: {metrics.win_rate_gap:.2f}" if metrics.win_rate_gap is not None else "  Win Rate Gap: N/A")
    lines.append(f"  Trade Count Gap: {metrics.trade_count_gap}")
    lines.append(f"  Direction: {metrics.gap_direction.value}")
    return "\n".join(lines)
