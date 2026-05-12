from datetime import datetime, timezone
from typing import List, Optional, Tuple, Union

from usa_signal_bot.core.enums import (
    PerformanceBaselineScope,
    PerformanceMetricName,
    SLAThresholdType,
    SLASeverity,
    BaselineComparisonStatus
)
from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample, PerformanceBaseline
from usa_signal_bot.performance.threshold_models import (
    SLAThreshold,
    SLAThresholdEvaluation,
    SLAEvaluationReport,
    create_sla_threshold_id,
    create_sla_evaluation_id,
    create_sla_report_id
)


def default_sla_thresholds() -> List[SLAThreshold]:
    return [
        SLAThreshold(create_sla_threshold_id(PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS), "Scan Time", PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS, SLAThresholdType.MAX, 1800, 3600, 7200, True, SLASeverity.WARNING),
        SLAThreshold(create_sla_threshold_id(PerformanceBaselineScope.BACKTEST, PerformanceMetricName.WALL_TIME_SECONDS), "Backtest Time", PerformanceBaselineScope.BACKTEST, PerformanceMetricName.WALL_TIME_SECONDS, SLAThresholdType.MAX, 7200, 14400, 21600, True, SLASeverity.WARNING),
        SLAThreshold(create_sla_threshold_id(PerformanceBaselineScope.REGRESSION, PerformanceMetricName.WALL_TIME_SECONDS), "Regression Time", PerformanceBaselineScope.REGRESSION, PerformanceMetricName.WALL_TIME_SECONDS, SLAThresholdType.MAX, 3600, 7200, 10800, True, SLASeverity.WARNING),
        SLAThreshold(create_sla_threshold_id(PerformanceBaselineScope.FULL_LOCAL_STACK, PerformanceMetricName.MEMORY_PEAK_MB), "Peak Memory", PerformanceBaselineScope.FULL_LOCAL_STACK, PerformanceMetricName.MEMORY_PEAK_MB, SLAThresholdType.MAX, 4096, 6144, 8192, True, SLASeverity.CRITICAL),
        SLAThreshold(create_sla_threshold_id(PerformanceBaselineScope.FULL_LOCAL_STACK, PerformanceMetricName.OUTPUT_GROWTH_MB), "Output Growth", PerformanceBaselineScope.FULL_LOCAL_STACK, PerformanceMetricName.OUTPUT_GROWTH_MB, SLAThresholdType.MAX, 512, 2048, 4096, True, SLASeverity.WARNING),
        SLAThreshold(create_sla_threshold_id(PerformanceBaselineScope.FULL_LOCAL_STACK, PerformanceMetricName.ERROR_COUNT), "Error Count", PerformanceBaselineScope.FULL_LOCAL_STACK, PerformanceMetricName.ERROR_COUNT, SLAThresholdType.MAX, 1, 5, 10, True, SLASeverity.ERROR),
        SLAThreshold(create_sla_threshold_id(PerformanceBaselineScope.FULL_LOCAL_STACK, PerformanceMetricName.FAILED_STEP_COUNT), "Failed Steps", PerformanceBaselineScope.FULL_LOCAL_STACK, PerformanceMetricName.FAILED_STEP_COUNT, SLAThresholdType.MAX, 1, 3, 5, True, SLASeverity.ERROR),
    ]

def thresholds_for_scope(scope: PerformanceBaselineScope, thresholds: Optional[List[SLAThreshold]] = None) -> List[SLAThreshold]:
    all_t = thresholds if thresholds is not None else default_sla_thresholds()
    return [t for t in all_t if t.scope == scope or t.scope == PerformanceBaselineScope.FULL_LOCAL_STACK]

def compare_observed_to_threshold(observed: Union[float, str, None], threshold: SLAThreshold, baseline_value: Union[float, str, None] = None) -> Tuple[BaselineComparisonStatus, SLASeverity, str]:
    if observed is None:
        return BaselineComparisonStatus.INSUFFICIENT_DATA, SLASeverity.INFO, "Missing observed data."

    if not threshold.enabled:
        return BaselineComparisonStatus.PASS, SLASeverity.INFO, "Threshold check disabled."

    if threshold.threshold_type == SLAThresholdType.MAX and isinstance(observed, (int, float)):
        val = float(observed)
        if threshold.blocker_value is not None and val >= float(threshold.blocker_value):
            return BaselineComparisonStatus.BLOCKED, SLASeverity.BLOCKER, f"Observed {val} exceeds BLOCKER max {threshold.blocker_value}."
        if threshold.critical_value is not None and val >= float(threshold.critical_value):
            return BaselineComparisonStatus.FAIL, SLASeverity.CRITICAL, f"Observed {val} exceeds CRITICAL max {threshold.critical_value}."
        if threshold.warning_value is not None and val >= float(threshold.warning_value):
            return BaselineComparisonStatus.WARN, SLASeverity.WARNING, f"Observed {val} exceeds WARNING max {threshold.warning_value}."
        return BaselineComparisonStatus.PASS, SLASeverity.INFO, f"Observed {val} is within acceptable limits."

    return BaselineComparisonStatus.PASS, SLASeverity.INFO, "Threshold check passed (unsupported type/type mismatch handled gracefully)."

def evaluate_threshold(threshold: SLAThreshold, sample: CurrentPerformanceSample, baseline: Optional[PerformanceBaseline] = None) -> SLAThresholdEvaluation:
    observed = sample.metrics.get(threshold.metric_name.value)

    baseline_value = None
    if baseline:
        for m in baseline.metrics:
            if m.name == threshold.metric_name:
                baseline_value = m.p90_value
                break

    status, severity, message = compare_observed_to_threshold(observed, threshold, baseline_value)

    return SLAThresholdEvaluation(
        evaluation_id=create_sla_evaluation_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        threshold_id=threshold.threshold_id,
        scope=threshold.scope,
        metric_name=threshold.metric_name,
        observed_value=observed,
        baseline_value=baseline_value,
        status=status,
        severity=severity,
        message=message,
        evidence={"sample_id": sample.sample_id, "baseline_id": baseline.baseline_id if baseline else None},
        warnings=[], errors=[]
    )

def evaluate_thresholds(scope: PerformanceBaselineScope, sample: CurrentPerformanceSample, baseline: Optional[PerformanceBaseline], thresholds: Optional[List[SLAThreshold]] = None) -> SLAEvaluationReport:
    active_thresholds = thresholds_for_scope(scope, thresholds)
    evaluations = [evaluate_threshold(t, sample, baseline) for t in active_thresholds]

    pass_count = sum(1 for e in evaluations if e.status == BaselineComparisonStatus.PASS)
    warn_count = sum(1 for e in evaluations if e.status == BaselineComparisonStatus.WARN)
    fail_count = sum(1 for e in evaluations if e.status == BaselineComparisonStatus.FAIL)
    blocked_count = sum(1 for e in evaluations if e.status == BaselineComparisonStatus.BLOCKED)

    overall = BaselineComparisonStatus.PASS
    if blocked_count > 0: overall = BaselineComparisonStatus.BLOCKED
    elif fail_count > 0: overall = BaselineComparisonStatus.FAIL
    elif warn_count > 0: overall = BaselineComparisonStatus.WARN

    return SLAEvaluationReport(
        report_id=create_sla_report_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        scope=scope,
        status=overall,
        evaluations=evaluations,
        pass_count=pass_count,
        warn_count=warn_count,
        fail_count=fail_count,
        blocked_count=blocked_count,
        warnings=[], errors=[]
    )

def sla_evaluation_report_to_text(report: SLAEvaluationReport) -> str:
    lines = [f"SLA Evaluation Report [{report.status.value}]"]
    lines.append(f"Pass: {report.pass_count}, Warn: {report.warn_count}, Fail: {report.fail_count}, Blocked: {report.blocked_count}")
    for e in report.evaluations:
        lines.append(f" - {e.metric_name.value}: {e.status.value} ({e.message})")
    lines.append("\nNote: SLA PASS is not an approval for live trading. This is a local operational baseline.")
    return "\n".join(lines)
