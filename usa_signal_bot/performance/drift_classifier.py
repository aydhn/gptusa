from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import BaselineDriftDirection, RuntimeRegressionStatus, BaselineComparisonStatus, SLASeverity
from usa_signal_bot.performance.threshold_models import SLAEvaluationReport

def classify_baseline_drift(metric_results: List[Dict[str, Any]]) -> BaselineDriftDirection:
    if not metric_results:
        return BaselineDriftDirection.UNKNOWN

    better_count = 0
    worse_count = 0
    flat_count = 0

    for r in metric_results:
        delta = r.get("delta_pct")
        if delta is None:
            continue

        # For our metrics (time, memory, size, errors), lower is better.
        if delta < -5.0:
            better_count += 1
        elif delta > 5.0:
            worse_count += 1
        else:
            flat_count += 1

    if better_count > 0 and worse_count > 0:
        return BaselineDriftDirection.MIXED
    elif worse_count > 0:
        return BaselineDriftDirection.WORSE
    elif better_count > 0:
        return BaselineDriftDirection.BETTER
    elif flat_count > 0:
        return BaselineDriftDirection.FLAT

    return BaselineDriftDirection.UNKNOWN

def classify_runtime_regression(metric_results: List[Dict[str, Any]], threshold_report: Optional[SLAEvaluationReport] = None) -> RuntimeRegressionStatus:
    if not metric_results:
        return RuntimeRegressionStatus.INSUFFICIENT_DATA

    if threshold_report:
        has_critical_sla = any(e.severity in [SLASeverity.CRITICAL, SLASeverity.BLOCKER] for e in threshold_report.evaluations if e.status in [BaselineComparisonStatus.FAIL, BaselineComparisonStatus.BLOCKED])
        if has_critical_sla:
            return RuntimeRegressionStatus.CRITICAL_REGRESSION

    has_blocked = any(r["status"] == BaselineComparisonStatus.BLOCKED.value for r in metric_results)
    if has_blocked:
        return RuntimeRegressionStatus.CRITICAL_REGRESSION

    has_fail = any(r["status"] == BaselineComparisonStatus.FAIL.value for r in metric_results)
    if has_fail:
        return RuntimeRegressionStatus.MAJOR_REGRESSION

    has_warn = any(r["status"] == BaselineComparisonStatus.WARN.value for r in metric_results)
    if has_warn:
        return RuntimeRegressionStatus.MODERATE_REGRESSION

    # Check for minor regression (positive delta but below warning threshold)
    has_minor = any(r.get("delta_pct") is not None and r["delta_pct"] > 5.0 for r in metric_results)
    if has_minor:
        return RuntimeRegressionStatus.MINOR_REGRESSION

    return RuntimeRegressionStatus.NO_REGRESSION

def drift_score_from_metric_results(metric_results: List[Dict[str, Any]]) -> float:
    score = 0.0
    valid_count = 0
    for r in metric_results:
        delta = r.get("delta_pct")
        if delta is not None:
            score += delta
            valid_count += 1
    return (score / valid_count) if valid_count > 0 else 0.0

def summarize_drift_reasons(metric_results: List[Dict[str, Any]]) -> List[str]:
    reasons = []
    for r in metric_results:
        delta = r.get("delta_pct")
        if delta is not None and delta > 5.0:
            reasons.append(f"{r['metric_name']} increased by {delta:.1f}%")
        elif delta is not None and delta < -5.0:
            reasons.append(f"{r['metric_name']} decreased by {abs(delta):.1f}%")
    return reasons

def runtime_regression_status_to_text(status: RuntimeRegressionStatus) -> str:
    return f"Regression Status: {status.value}"
