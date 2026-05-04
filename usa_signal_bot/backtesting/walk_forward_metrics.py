from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.enums import WalkForwardMetricStatus, WalkForwardStabilityBucket, OutOfSampleResultBucket
from usa_signal_bot.backtesting.walk_forward_models import WalkForwardWindowResult

@dataclass
class WalkForwardAggregateMetrics:
    status: WalkForwardMetricStatus
    total_windows: int
    completed_windows: int
    failed_windows: int
    average_in_sample_return_pct: float | None
    average_out_of_sample_return_pct: float | None
    median_out_of_sample_return_pct: float | None
    oos_positive_window_ratio: float | None
    oos_win_rate_average: float | None
    average_degradation_pct: float | None
    worst_oos_return_pct: float | None
    best_oos_return_pct: float | None
    average_oos_max_drawdown_pct: float | None
    stability_score: float | None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def extract_metric_value(metrics: dict[str, Any], key: str) -> float | None:
    return metrics.get(key)

def calculate_degradation(in_sample_return: float | None, out_sample_return: float | None) -> float | None:
    if in_sample_return is None or out_sample_return is None:
        return None
    # Degradation measures how much worse OOS is compared to IS
    # E.g., IS=10%, OOS=5% -> degradation = -5%
    return out_sample_return - in_sample_return

def calculate_oos_positive_window_ratio(results: list[WalkForwardWindowResult]) -> float | None:
    completed = [r for r in results if r.out_of_sample_result_id is not None]
    if not completed:
        return None

    positive_count = 0
    for r in completed:
        oos_ret = extract_metric_value(r.out_of_sample_metrics, "total_return_pct")
        if oos_ret is not None and oos_ret > 0:
            positive_count += 1

    return positive_count / len(completed)

def calculate_average_degradation(results: list[WalkForwardWindowResult]) -> float | None:
    completed = [r for r in results if r.in_sample_result_id is not None and r.out_of_sample_result_id is not None]
    if not completed:
        return None

    degradations = []
    for r in completed:
        is_ret = extract_metric_value(r.in_sample_metrics, "total_return_pct")
        oos_ret = extract_metric_value(r.out_of_sample_metrics, "total_return_pct")
        deg = calculate_degradation(is_ret, oos_ret)
        if deg is not None:
            degradations.append(deg)

    if not degradations:
        return None

    return sum(degradations) / len(degradations)

def calculate_stability_score(results: list[WalkForwardWindowResult]) -> float | None:
    completed = [r for r in results if r.out_of_sample_result_id is not None]
    if len(completed) < 2:
        return None

    # Basic stability score 0-100 based on OOS positive ratio and degradation
    pos_ratio = calculate_oos_positive_window_ratio(completed)
    avg_deg = calculate_average_degradation(completed)

    if pos_ratio is None or avg_deg is None:
        return None

    # Start at 50, add points for positive ratio, penalize for degradation
    score = 50.0 + ((pos_ratio - 0.5) * 50.0) # 0.0 -> 25, 1.0 -> 75

    # Penalize if OOS is significantly worse than IS
    if avg_deg < 0:
        # e.g., -5% degradation -> subtract 5 points
        score += max(-40.0, avg_deg)

    return max(0.0, min(100.0, score))

def classify_walk_forward_stability(score: float | None) -> WalkForwardStabilityBucket:
    if score is None:
        return WalkForwardStabilityBucket.INSUFFICIENT_DATA
    if score >= 75.0:
        return WalkForwardStabilityBucket.STABLE
    elif score >= 50.0:
        return WalkForwardStabilityBucket.MODERATE
    elif score >= 25.0:
        return WalkForwardStabilityBucket.UNSTABLE
    else:
        return WalkForwardStabilityBucket.SEVERELY_UNSTABLE

def classify_out_of_sample_result(metrics: WalkForwardAggregateMetrics) -> OutOfSampleResultBucket:

    if isinstance(metrics, dict):
        status = metrics.get('status')
        pos_ratio = metrics.get('oos_positive_window_ratio')
        avg_oos = metrics.get('average_out_of_sample_return_pct')
    else:
        status = metrics.status
        pos_ratio = metrics.oos_positive_window_ratio
        avg_oos = metrics.average_out_of_sample_return_pct

    if status == WalkForwardMetricStatus.EMPTY or status == "EMPTY":

         return OutOfSampleResultBucket.INSUFFICIENT_DATA

    # pos_ratio done above
    # avg_oos done above

    if pos_ratio is None or avg_oos is None:
        return OutOfSampleResultBucket.UNKNOWN

    if pos_ratio >= 0.6 and avg_oos > 5.0:
        return OutOfSampleResultBucket.STRONG
    elif pos_ratio >= 0.4 and avg_oos > 0.0:
        return OutOfSampleResultBucket.ACCEPTABLE
    elif pos_ratio >= 0.2:
        return OutOfSampleResultBucket.WEAK
    else:
        return OutOfSampleResultBucket.FAILED

def calculate_walk_forward_aggregate_metrics(results: list[WalkForwardWindowResult]) -> WalkForwardAggregateMetrics:
    if not results:
        return WalkForwardAggregateMetrics(
            status=WalkForwardMetricStatus.EMPTY,
            total_windows=0, completed_windows=0, failed_windows=0,
            average_in_sample_return_pct=None, average_out_of_sample_return_pct=None,
            median_out_of_sample_return_pct=None, oos_positive_window_ratio=None,
            oos_win_rate_average=None, average_degradation_pct=None,
            worst_oos_return_pct=None, best_oos_return_pct=None,
            average_oos_max_drawdown_pct=None, stability_score=None,
            warnings=["No results provided"]
        )

    total_windows = len(results)
    failed_windows = sum(1 for r in results if r.in_sample_result_id is None and r.out_of_sample_result_id is None)
    completed_windows = total_windows - failed_windows

    if completed_windows == 0:
        return WalkForwardAggregateMetrics(
            status=WalkForwardMetricStatus.EMPTY,
            total_windows=total_windows, completed_windows=0, failed_windows=failed_windows,
            average_in_sample_return_pct=None, average_out_of_sample_return_pct=None,
            median_out_of_sample_return_pct=None, oos_positive_window_ratio=None,
            oos_win_rate_average=None, average_degradation_pct=None,
            worst_oos_return_pct=None, best_oos_return_pct=None,
            average_oos_max_drawdown_pct=None, stability_score=None,
            warnings=["All windows failed or were skipped"]
        )

    is_returns = []
    oos_returns = []
    oos_win_rates = []
    oos_dd = []

    for r in results:
        if r.in_sample_result_id:
            val = extract_metric_value(r.in_sample_metrics, "total_return_pct")
            if val is not None: is_returns.append(val)

        if r.out_of_sample_result_id:
            val = extract_metric_value(r.out_of_sample_metrics, "total_return_pct")
            if val is not None: oos_returns.append(val)

            wr = extract_metric_value(r.out_of_sample_metrics, "win_rate_pct")
            if wr is not None: oos_win_rates.append(wr)

            dd = extract_metric_value(r.out_of_sample_metrics, "max_drawdown_pct")
            if dd is not None: oos_dd.append(dd)

    avg_is = sum(is_returns) / len(is_returns) if is_returns else None
    avg_oos = sum(oos_returns) / len(oos_returns) if oos_returns else None

    median_oos = None
    if oos_returns:
        s_oos = sorted(oos_returns)
        n = len(s_oos)
        if n % 2 == 1:
            median_oos = s_oos[n//2]
        else:
            median_oos = (s_oos[n//2 - 1] + s_oos[n//2]) / 2.0

    worst_oos = min(oos_returns) if oos_returns else None
    best_oos = max(oos_returns) if oos_returns else None

    avg_oos_wr = sum(oos_win_rates) / len(oos_win_rates) if oos_win_rates else None
    avg_oos_dd = sum(oos_dd) / len(oos_dd) if oos_dd else None

    oos_pos_ratio = calculate_oos_positive_window_ratio(results)
    avg_deg = calculate_average_degradation(results)
    stab_score = calculate_stability_score(results)

    status = WalkForwardMetricStatus.OK
    if completed_windows < total_windows:
        status = WalkForwardMetricStatus.WARNING

    return WalkForwardAggregateMetrics(
        status=status,
        total_windows=total_windows,
        completed_windows=completed_windows,
        failed_windows=failed_windows,
        average_in_sample_return_pct=avg_is,
        average_out_of_sample_return_pct=avg_oos,
        median_out_of_sample_return_pct=median_oos,
        oos_positive_window_ratio=oos_pos_ratio,
        oos_win_rate_average=avg_oos_wr,
        average_degradation_pct=avg_deg,
        worst_oos_return_pct=worst_oos,
        best_oos_return_pct=best_oos,
        average_oos_max_drawdown_pct=avg_oos_dd,
        stability_score=stab_score
    )

def walk_forward_aggregate_metrics_to_dict(metrics: WalkForwardAggregateMetrics) -> dict:
    return {
        "status": metrics.status.value if isinstance(metrics.status, WalkForwardMetricStatus) else metrics.status,
        "total_windows": metrics.total_windows,
        "completed_windows": metrics.completed_windows,
        "failed_windows": metrics.failed_windows,
        "average_in_sample_return_pct": metrics.average_in_sample_return_pct,
        "average_out_of_sample_return_pct": metrics.average_out_of_sample_return_pct,
        "median_out_of_sample_return_pct": metrics.median_out_of_sample_return_pct,
        "oos_positive_window_ratio": metrics.oos_positive_window_ratio,
        "oos_win_rate_average": metrics.oos_win_rate_average,
        "average_degradation_pct": metrics.average_degradation_pct,
        "worst_oos_return_pct": metrics.worst_oos_return_pct,
        "best_oos_return_pct": metrics.best_oos_return_pct,
        "average_oos_max_drawdown_pct": metrics.average_oos_max_drawdown_pct,
        "stability_score": metrics.stability_score,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def walk_forward_aggregate_metrics_to_text(metrics: WalkForwardAggregateMetrics) -> str:
    lines = []
    lines.append("Walk-Forward Aggregate Metrics:")
    if isinstance(metrics, dict):
        lines.append(f"  Status:                    {metrics.get('status')}")
        lines.append(f"  Total Windows:             {metrics.get('total_windows')}")
        lines.append(f"  Completed/Failed:          {metrics.get('completed_windows')} / {metrics.get('failed_windows')}")

        def fmt(val):
            return f"{val:.2f}%" if val is not None else "N/A"

        lines.append(f"  Average IS Return:         {fmt(metrics.get('average_in_sample_return_pct'))}")
        lines.append(f"  Average OOS Return:        {fmt(metrics.get('average_out_of_sample_return_pct'))}")
        lines.append(f"  Median OOS Return:         {fmt(metrics.get('median_out_of_sample_return_pct'))}")
        lines.append(f"  Worst OOS Return:          {fmt(metrics.get('worst_oos_return_pct'))}")
        lines.append(f"  Best OOS Return:           {fmt(metrics.get('best_oos_return_pct'))}")

        lines.append(f"  Average Degradation:       {fmt(metrics.get('average_degradation_pct'))}")

        opr = metrics.get('oos_positive_window_ratio')
        lines.append(f"  OOS Positive Window Ratio: {opr:.2f}" if opr is not None else "  OOS Positive Window Ratio: N/A")
        lines.append(f"  OOS Win Rate Average:      {fmt(metrics.get('oos_win_rate_average'))}")

        ss = metrics.get('stability_score')
        lines.append(f"  Stability Score:           {ss:.1f}/100" if ss is not None else "  Stability Score:           N/A")

        warns = metrics.get('warnings', [])
        if warns:
            lines.append(f"  Warnings: {len(warns)}")
        return "\n".join(lines)

    lines.append(f"  Status:                    {metrics.status.value}")
    lines.append(f"  Total Windows:             {metrics.total_windows}")
    lines.append(f"  Completed/Failed:          {metrics.completed_windows} / {metrics.failed_windows}")

    def fmt(val):
        return f"{val:.2f}%" if val is not None else "N/A"

    lines.append(f"  Average IS Return:         {fmt(metrics.average_in_sample_return_pct)}")
    lines.append(f"  Average OOS Return:        {fmt(metrics.average_out_of_sample_return_pct)}")
    lines.append(f"  Median OOS Return:         {fmt(metrics.median_out_of_sample_return_pct)}")
    lines.append(f"  Worst OOS Return:          {fmt(metrics.worst_oos_return_pct)}")
    lines.append(f"  Best OOS Return:           {fmt(metrics.best_oos_return_pct)}")

    lines.append(f"  Average Degradation:       {fmt(metrics.average_degradation_pct)}")
    lines.append(f"  OOS Positive Window Ratio: {metrics.oos_positive_window_ratio:.2f}" if metrics.oos_positive_window_ratio is not None else "  OOS Positive Window Ratio: N/A")
    lines.append(f"  OOS Win Rate Average:      {fmt(metrics.oos_win_rate_average)}")
    lines.append(f"  Stability Score:           {metrics.stability_score:.1f}/100" if metrics.stability_score is not None else "  Stability Score:           N/A")

    if metrics.warnings:
        lines.append(f"  Warnings: {len(metrics.warnings)}")

    return "\n".join(lines)
