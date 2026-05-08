from typing import List, Optional, Any
from usa_signal_bot.core.enums import ComparisonMetricStatus, ExecutionRealismBucket, GapSeverity, MatchStatus
from usa_signal_bot.comparison.comparison_models import ExecutionGapMetrics, MatchedTradePair, PerformanceGapMetrics, SignalDriftMetrics
from usa_signal_bot.comparison.timing_gap import estimate_timing_gap_bars

def calculate_execution_gap_metrics(matched_trades: List[MatchedTradePair], matched_order_fills: Optional[List[Any]] = None) -> ExecutionGapMetrics:
    matched_count = sum(1 for p in matched_trades if p.match_status == MatchStatus.MATCHED)
    unmatched_p = sum(1 for p in matched_trades if p.match_status == MatchStatus.PAPER_ONLY)
    unmatched_b = sum(1 for p in matched_trades if p.match_status == MatchStatus.BACKTEST_ONLY)

    avg_entry_gap = calculate_average_price_gap_from_matches(matched_trades, entry=True)
    avg_exit_gap = calculate_average_price_gap_from_matches(matched_trades, entry=False)
    avg_timing_gap = calculate_average_timing_gap_from_matches(matched_trades)
    avg_pnl_gap = calculate_average_pnl_gap_from_matches(matched_trades)

    # Missing fill count basic heuristic
    missing_fills = 0
    total_fee_gap = 0.0
    total_slip_gap = 0.0
    if matched_order_fills:
        for f in matched_order_fills:
            if f.match_status in (MatchStatus.PAPER_ONLY, MatchStatus.BACKTEST_ONLY):
                missing_fills += 1
            if f.fee_gap is not None:
                total_fee_gap += f.fee_gap

    status = ComparisonMetricStatus.OK if matched_count > 0 else ComparisonMetricStatus.INSUFFICIENT_DATA

    metrics = ExecutionGapMetrics(
        status=status,
        matched_trade_count=matched_count,
        unmatched_paper_count=unmatched_p,
        unmatched_backtest_count=unmatched_b,
        average_entry_price_gap_pct=avg_entry_gap,
        average_exit_price_gap_pct=avg_exit_gap,
        average_timing_gap_bars=avg_timing_gap,
        average_pnl_gap=avg_pnl_gap,
        total_fee_gap=total_fee_gap if matched_order_fills else None,
        total_slippage_gap=total_slip_gap if matched_order_fills else None,
        missing_fill_count=missing_fills,
        execution_realism_score=None,
        execution_realism_bucket=ExecutionRealismBucket.UNKNOWN,
        warnings=[],
        errors=[]
    )

    metrics.execution_realism_score = calculate_execution_realism_score(metrics)
    metrics.execution_realism_bucket = classify_execution_realism_bucket(metrics.execution_realism_score, metrics)
    return metrics

def calculate_average_price_gap_from_matches(matched_trades: List[MatchedTradePair], entry: bool = True) -> Optional[float]:
    gaps = []
    for p in matched_trades:
        if p.match_status == MatchStatus.MATCHED:
            if entry:
                v1, v2 = p.paper_entry_price, p.backtest_entry_price
            else:
                v1, v2 = p.paper_exit_price, p.backtest_exit_price

            if v1 is not None and v2 is not None and v2 != 0:
                gaps.append(abs((v1 - v2) / v2 * 100.0))
    return sum(gaps) / len(gaps) if gaps else None

def calculate_average_timing_gap_from_matches(matched_trades: List[MatchedTradePair]) -> Optional[float]:
    gaps = []
    for p in matched_trades:
        if p.match_status == MatchStatus.MATCHED:
            e = estimate_timing_gap_bars(p.paper_entry_time, p.backtest_entry_time, p.timeframe)
            if e is not None:
                gaps.append(e)
    return sum(gaps) / len(gaps) if gaps else None

def calculate_average_pnl_gap_from_matches(matched_trades: List[MatchedTradePair]) -> Optional[float]:
    gaps = []
    for p in matched_trades:
        if p.match_status == MatchStatus.MATCHED:
            if p.paper_net_pnl is not None and p.backtest_net_pnl is not None:
                gaps.append(abs(p.paper_net_pnl - p.backtest_net_pnl))
    return sum(gaps) / len(gaps) if gaps else None

def calculate_execution_realism_score(metrics: ExecutionGapMetrics) -> Optional[float]:
    if metrics.status == ComparisonMetricStatus.INSUFFICIENT_DATA or metrics.matched_trade_count == 0:
        return None

    score = 100.0

    # Penalize for unmatched trades
    total = metrics.matched_trade_count + metrics.unmatched_paper_count + metrics.unmatched_backtest_count
    if total > 0:
        unmatched_ratio = (metrics.unmatched_paper_count + metrics.unmatched_backtest_count) / total
        score -= (unmatched_ratio * 40.0)

    # Penalize for price gap
    if metrics.average_entry_price_gap_pct is not None:
        score -= min(30.0, metrics.average_entry_price_gap_pct * 10.0)

    # Penalize for timing gap
    if metrics.average_timing_gap_bars is not None:
        score -= min(30.0, metrics.average_timing_gap_bars * 5.0)

    return max(0.0, min(100.0, score))

def classify_execution_realism_bucket(score: Optional[float], metrics: Optional[ExecutionGapMetrics] = None) -> ExecutionRealismBucket:
    if score is None:
        return ExecutionRealismBucket.INSUFFICIENT_DATA
    if score >= 90:
        return ExecutionRealismBucket.HIGH_REALISM
    if score >= 70:
        return ExecutionRealismBucket.ACCEPTABLE_REALISM
    if score >= 50:
        return ExecutionRealismBucket.MODERATE_GAP
    if score >= 30:
        return ExecutionRealismBucket.LARGE_GAP
    return ExecutionRealismBucket.SEVERE_GAP

def classify_overall_gap_severity(performance_gap: PerformanceGapMetrics, execution_gap: ExecutionGapMetrics, signal_drift: Optional[SignalDriftMetrics] = None) -> GapSeverity:
    severities = []

    # Check perf gap
    if performance_gap.total_return_gap_pct is not None:
        if abs(performance_gap.total_return_gap_pct) > 10.0:
            severities.append(GapSeverity.CRITICAL)
        elif abs(performance_gap.total_return_gap_pct) > 5.0:
            severities.append(GapSeverity.HIGH)

    # Check execution realism
    b = execution_gap.execution_realism_bucket
    if b == ExecutionRealismBucket.SEVERE_GAP:
        severities.append(GapSeverity.CRITICAL)
    elif b == ExecutionRealismBucket.LARGE_GAP:
        severities.append(GapSeverity.HIGH)
    elif b == ExecutionRealismBucket.MODERATE_GAP:
        severities.append(GapSeverity.MODERATE)

    if GapSeverity.CRITICAL in severities:
        return GapSeverity.CRITICAL
    if GapSeverity.HIGH in severities:
        return GapSeverity.HIGH
    if GapSeverity.MODERATE in severities:
        return GapSeverity.MODERATE

    return GapSeverity.LOW

def execution_gap_metrics_to_text(metrics: ExecutionGapMetrics) -> str:
    lines = ["Execution Gap Metrics:"]
    lines.append(f"  Matched Trades: {metrics.matched_trade_count}")
    lines.append(f"  Unmatched Paper: {metrics.unmatched_paper_count}")
    lines.append(f"  Unmatched Backtest: {metrics.unmatched_backtest_count}")
    lines.append(f"  Realism Score: {metrics.execution_realism_score:.1f}" if metrics.execution_realism_score is not None else "  Realism Score: N/A")
    lines.append(f"  Bucket: {metrics.execution_realism_bucket.value}")
    return "\n".join(lines)
