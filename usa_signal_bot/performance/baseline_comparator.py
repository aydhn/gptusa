from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName, BaselineComparisonStatus, BaselineDriftDirection, RuntimeRegressionStatus
from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample, PerformanceBaseline, PerformanceMetricBaseline, BaselineComparisonResult, create_baseline_comparison_id

def calculate_delta_pct(observed: Optional[float], baseline_value: Optional[float]) -> Optional[float]:
    if observed is None or baseline_value is None or baseline_value == 0:
        return None
    return ((observed - baseline_value) / baseline_value) * 100.0

def compare_metric_to_baseline(metric_name: PerformanceMetricName, observed: Any, metric_baseline: Optional[PerformanceMetricBaseline]) -> Dict[str, Any]:
    if metric_baseline is None or observed is None or metric_baseline.p90_value is None:
        return {
            "metric_name": metric_name.value,
            "observed": observed,
            "baseline_p90": None,
            "delta_pct": None,
            "status": BaselineComparisonStatus.INSUFFICIENT_DATA.value
        }

    if not isinstance(observed, (int, float)):
        return {
            "metric_name": metric_name.value,
            "observed": observed,
            "baseline_p90": metric_baseline.p90_value,
            "delta_pct": None,
            "status": BaselineComparisonStatus.UNKNOWN.value
        }

    obs_val = float(observed)
    base_val = metric_baseline.p90_value
    delta = calculate_delta_pct(obs_val, base_val)

    status = BaselineComparisonStatus.PASS
    if delta is not None:
        if delta > 100.0:
            status = BaselineComparisonStatus.BLOCKED
        elif delta > 50.0:
            status = BaselineComparisonStatus.FAIL
        elif delta > 25.0:
            status = BaselineComparisonStatus.WARN

    if metric_name in [PerformanceMetricName.ERROR_COUNT, PerformanceMetricName.FAILED_STEP_COUNT] and obs_val > 0:
        # Errors produce stricter statuses intrinsically
        if obs_val > base_val * 2: status = BaselineComparisonStatus.BLOCKED
        elif obs_val > base_val: status = BaselineComparisonStatus.FAIL

    return {
        "metric_name": metric_name.value,
        "observed": obs_val,
        "baseline_p90": base_val,
        "delta_pct": delta,
        "status": status.value
    }

def find_baseline_for_sample(sample: CurrentPerformanceSample, baselines: List[PerformanceBaseline]) -> Optional[PerformanceBaseline]:
    for b in baselines:
        if b.scope == sample.scope:
            return b
    return None

def classify_comparison_status(metric_results: List[Dict[str, Any]]) -> BaselineComparisonStatus:
    has_blocked = any(r["status"] == BaselineComparisonStatus.BLOCKED.value for r in metric_results)
    if has_blocked: return BaselineComparisonStatus.BLOCKED

    has_fail = any(r["status"] == BaselineComparisonStatus.FAIL.value for r in metric_results)
    if has_fail: return BaselineComparisonStatus.FAIL

    has_warn = any(r["status"] == BaselineComparisonStatus.WARN.value for r in metric_results)
    if has_warn: return BaselineComparisonStatus.WARN

    has_insufficient = all(r["status"] == BaselineComparisonStatus.INSUFFICIENT_DATA.value for r in metric_results)
    if has_insufficient and metric_results: return BaselineComparisonStatus.INSUFFICIENT_DATA

    return BaselineComparisonStatus.PASS

def compare_sample_to_baseline(sample: CurrentPerformanceSample, baseline: Optional[PerformanceBaseline]) -> BaselineComparisonResult:
    results = []

    for metric_name_val, observed in sample.metrics.items():
        try:
            m_name = PerformanceMetricName(metric_name_val)
        except ValueError:
            continue

        m_base = None
        if baseline:
            for mb in baseline.metrics:
                if mb.name == m_name:
                    m_base = mb
                    break

        results.append(compare_metric_to_baseline(m_name, observed, m_base))

    status = classify_comparison_status(results)

    # Defaults; to be filled by drift classifier in regression pipeline
    drift = BaselineDriftDirection.UNKNOWN
    reg = RuntimeRegressionStatus.UNKNOWN

    return BaselineComparisonResult(
        comparison_id=create_baseline_comparison_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        scope=sample.scope,
        status=status,
        baseline_id=baseline.baseline_id if baseline else None,
        sample_id=sample.sample_id,
        metric_results=results,
        drift_direction=drift,
        regression_status=reg,
        warnings=[], errors=[]
    )

def compare_samples_to_baselines(samples: List[CurrentPerformanceSample], baselines: List[PerformanceBaseline]) -> List[BaselineComparisonResult]:
    return [compare_sample_to_baseline(s, find_baseline_for_sample(s, baselines)) for s in samples]

def baseline_comparison_result_to_text(result: BaselineComparisonResult, limit: int = 50) -> str:
    lines = [f"Baseline Comparison [{result.status.value}]"]
    for r in result.metric_results[:limit]:
        delta_str = f"{r['delta_pct']:.1f}%" if r['delta_pct'] is not None else "N/A"
        lines.append(f" - {r['metric_name']}: obs={r['observed']}, base_p90={r['baseline_p90']} (Delta: {delta_str}) -> {r['status']}")
    return "\n".join(lines)
