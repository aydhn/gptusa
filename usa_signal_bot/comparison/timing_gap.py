from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from usa_signal_bot.core.enums import ComparisonMetricStatus, GapSeverity, MatchStatus
from usa_signal_bot.comparison.comparison_models import MatchedTradePair

@dataclass
class TimingGapMetrics:
    status: ComparisonMetricStatus
    matched_count: int
    average_entry_timing_gap_bars: Optional[float]
    average_exit_timing_gap_bars: Optional[float]
    max_entry_timing_gap_bars: Optional[int]
    max_exit_timing_gap_bars: Optional[int]
    delayed_entry_count: int
    delayed_exit_count: int
    timing_gap_severity: GapSeverity
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def calculate_timing_gap_metrics(pairs: List[MatchedTradePair]) -> TimingGapMetrics:
    entry_gaps = []
    exit_gaps = []
    delayed_entry = 0
    delayed_exit = 0
    matched_count = 0

    for p in pairs:
        if p.match_status == MatchStatus.MATCHED:
            matched_count += 1
            e_gap = estimate_timing_gap_bars(p.paper_entry_time, p.backtest_entry_time, p.timeframe)
            if e_gap is not None:
                entry_gaps.append(e_gap)
                if e_gap > 0:
                    delayed_entry += 1

            ex_gap = estimate_timing_gap_bars(p.paper_exit_time, p.backtest_exit_time, p.timeframe)
            if ex_gap is not None:
                exit_gaps.append(ex_gap)
                if ex_gap > 0:
                    delayed_exit += 1

    avg_entry = sum(entry_gaps) / len(entry_gaps) if entry_gaps else None
    avg_exit = sum(exit_gaps) / len(exit_gaps) if exit_gaps else None
    max_entry = max(entry_gaps) if entry_gaps else None
    max_exit = max(exit_gaps) if exit_gaps else None

    metrics = TimingGapMetrics(
        status=ComparisonMetricStatus.OK if matched_count > 0 else ComparisonMetricStatus.INSUFFICIENT_DATA,
        matched_count=matched_count,
        average_entry_timing_gap_bars=avg_entry,
        average_exit_timing_gap_bars=avg_exit,
        max_entry_timing_gap_bars=max_entry,
        max_exit_timing_gap_bars=max_exit,
        delayed_entry_count=delayed_entry,
        delayed_exit_count=delayed_exit,
        timing_gap_severity=GapSeverity.UNKNOWN
    )
    metrics.timing_gap_severity = classify_timing_gap_severity(metrics)
    return metrics

def estimate_timing_gap_bars(time_a: Optional[str], time_b: Optional[str], timeframe: Optional[str] = None) -> Optional[int]:
    if not time_a or not time_b:
        return None
    try:
        da = datetime.fromisoformat(time_a).date()
        db = datetime.fromisoformat(time_b).date()
        diff_days = abs((da - db).days)
        # Approximate 1 bar = 1 day for this basic check if timeframe is daily or unknown
        # In a real impl, we'd use a trading calendar
        if timeframe in ["1w", "W"]:
            return diff_days // 7
        return diff_days
    except Exception:
        return None

def classify_timing_gap_severity(metrics: TimingGapMetrics, warning_bars: int = 1, critical_bars: int = 5) -> GapSeverity:
    if metrics.status == ComparisonMetricStatus.INSUFFICIENT_DATA:
        return GapSeverity.UNKNOWN

    m = max(metrics.max_entry_timing_gap_bars or 0, metrics.max_exit_timing_gap_bars or 0)

    if m >= critical_bars:
        return GapSeverity.CRITICAL
    if m >= warning_bars:
        return GapSeverity.MODERATE

    return GapSeverity.LOW

def timing_gap_metrics_to_dict(metrics: TimingGapMetrics) -> dict:
    from dataclasses import asdict
    d = asdict(metrics)
    if isinstance(d.get("status"), ComparisonMetricStatus):
        d["status"] = d["status"].value
    if isinstance(d.get("timing_gap_severity"), GapSeverity):
        d["timing_gap_severity"] = d["timing_gap_severity"].value
    return d

def timing_gap_metrics_to_text(metrics: TimingGapMetrics) -> str:
    lines = ["Timing Gap Metrics:"]
    lines.append(f"  Matched Trades: {metrics.matched_count}")
    lines.append(f"  Avg Entry Gap (Bars): {metrics.average_entry_timing_gap_bars:.2f}" if metrics.average_entry_timing_gap_bars is not None else "  Avg Entry Gap (Bars): N/A")
    lines.append(f"  Max Entry Gap (Bars): {metrics.max_entry_timing_gap_bars}" if metrics.max_entry_timing_gap_bars is not None else "  Max Entry Gap (Bars): N/A")
    lines.append(f"  Severity: {metrics.timing_gap_severity.value}")
    return "\n".join(lines)
