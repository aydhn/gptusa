from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import (
    PerformanceBaselineScope,
    PerformanceMetricName,
    BaselineStatus,
    BaselineComparisonStatus,
    RuntimeRegressionStatus,
    BaselineDriftDirection,
    PerformanceReportType
)
from usa_signal_bot.core.exceptions import PerformanceBaselineValidationError


@dataclass
class PerformanceMetricBaseline:
    metric_id: str
    name: PerformanceMetricName
    scope: PerformanceBaselineScope
    sample_count: int
    mean_value: Optional[float]
    median_value: Optional[float]
    p75_value: Optional[float]
    p90_value: Optional[float]
    min_value: Optional[float]
    max_value: Optional[float]
    unit: Optional[str]
    status: BaselineStatus
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceBaseline:
    baseline_id: str
    version: str
    scope: PerformanceBaselineScope
    status: BaselineStatus
    created_at_utc: str
    source_count: int
    metrics: List[PerformanceMetricBaseline]
    source_paths: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CurrentPerformanceSample:
    sample_id: str
    scope: PerformanceBaselineScope
    created_at_utc: str
    metrics: Dict[str, Any]
    source_path: Optional[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BaselineComparisonResult:
    comparison_id: str
    created_at_utc: str
    scope: PerformanceBaselineScope
    status: BaselineComparisonStatus
    baseline_id: Optional[str]
    sample_id: Optional[str]
    metric_results: List[Dict[str, Any]]
    drift_direction: BaselineDriftDirection
    regression_status: RuntimeRegressionStatus
    warnings: List[str]
    errors: List[str]


@dataclass
class PerformanceReviewResult:
    review_id: str
    created_at_utc: str
    report_type: PerformanceReportType
    status: BaselineComparisonStatus
    baselines: List[PerformanceBaseline]
    samples: List[CurrentPerformanceSample]
    comparisons: List[BaselineComparisonResult]
    threshold_results: List[Any]
    regression_alerts: List[Any]
    acceptance_status: BaselineComparisonStatus
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]


def create_performance_metric_baseline_id(name: PerformanceMetricName, scope: PerformanceBaselineScope) -> str:
    return f"metric_{scope.value.lower()}_{name.value.lower()}"


def create_performance_baseline_id(scope: PerformanceBaselineScope, prefix: str = "perf_base") -> str:
    return f"{prefix}_{scope.value.lower()}_{uuid.uuid4().hex[:8]}"


def create_current_performance_sample_id(scope: PerformanceBaselineScope, prefix: str = "perf_sample") -> str:
    return f"{prefix}_{scope.value.lower()}_{uuid.uuid4().hex[:8]}"


def create_baseline_comparison_id(prefix: str = "perf_compare") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def create_performance_review_id(prefix: str = "perf_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def validate_performance_metric_baseline(metric: PerformanceMetricBaseline) -> None:
    if metric.sample_count < 0:
        raise PerformanceBaselineValidationError("sample_count cannot be negative.")

    # Check numeric values are not negative, except for those where it's not applicable
    numeric_fields = ["mean_value", "median_value", "p75_value", "p90_value", "min_value", "max_value"]
    for f in numeric_fields:
        val = getattr(metric, f)
        if val is not None and val < 0:
            if metric.name not in [PerformanceMetricName.WARNING_COUNT, PerformanceMetricName.ERROR_COUNT, PerformanceMetricName.FAILED_STEP_COUNT, PerformanceMetricName.BLOCKED_STEP_COUNT]:
                raise PerformanceBaselineValidationError(f"{f} cannot be negative for metric {metric.name.value}.")
            else:
                 raise PerformanceBaselineValidationError(f"{f} cannot be negative for metric {metric.name.value}.")


def validate_performance_baseline(baseline: PerformanceBaseline) -> None:
    if not baseline.baseline_id:
        raise PerformanceBaselineValidationError("baseline_id cannot be empty.")
    if not baseline.version:
        raise PerformanceBaselineValidationError("version cannot be empty.")
    if baseline.source_count < 0:
        raise PerformanceBaselineValidationError("source_count cannot be negative.")
    for metric in baseline.metrics:
        validate_performance_metric_baseline(metric)


def validate_current_performance_sample(sample: CurrentPerformanceSample) -> None:
    if not sample.sample_id:
        raise PerformanceBaselineValidationError("sample_id cannot be empty.")
    for k, v in sample.metrics.items():
        if isinstance(v, (int, float)) and v < 0:
            raise PerformanceBaselineValidationError(f"Metric value for {k} cannot be negative.")


def validate_baseline_comparison_result(result: BaselineComparisonResult) -> None:
    if not result.comparison_id:
        raise PerformanceBaselineValidationError("comparison_id cannot be empty.")


def performance_metric_baseline_to_dict(metric: PerformanceMetricBaseline) -> Dict[str, Any]:
    return {
        "metric_id": metric.metric_id,
        "name": metric.name.value,
        "scope": metric.scope.value,
        "sample_count": metric.sample_count,
        "mean_value": metric.mean_value,
        "median_value": metric.median_value,
        "p75_value": metric.p75_value,
        "p90_value": metric.p90_value,
        "min_value": metric.min_value,
        "max_value": metric.max_value,
        "unit": metric.unit,
        "status": metric.status.value,
        "metadata": metric.metadata
    }


def performance_baseline_to_dict(baseline: PerformanceBaseline) -> Dict[str, Any]:
    return {
        "baseline_id": baseline.baseline_id,
        "version": baseline.version,
        "scope": baseline.scope.value,
        "status": baseline.status.value,
        "created_at_utc": baseline.created_at_utc,
        "source_count": baseline.source_count,
        "metrics": [performance_metric_baseline_to_dict(m) for m in baseline.metrics],
        "source_paths": baseline.source_paths,
        "warnings": baseline.warnings,
        "errors": baseline.errors,
        "metadata": baseline.metadata
    }


def current_performance_sample_to_dict(sample: CurrentPerformanceSample) -> Dict[str, Any]:
    return {
        "sample_id": sample.sample_id,
        "scope": sample.scope.value,
        "created_at_utc": sample.created_at_utc,
        "metrics": sample.metrics,
        "source_path": sample.source_path,
        "warnings": sample.warnings,
        "errors": sample.errors,
        "metadata": sample.metadata
    }


def baseline_comparison_result_to_dict(result: BaselineComparisonResult) -> Dict[str, Any]:
    return {
        "comparison_id": result.comparison_id,
        "created_at_utc": result.created_at_utc,
        "scope": result.scope.value,
        "status": result.status.value,
        "baseline_id": result.baseline_id,
        "sample_id": result.sample_id,
        "metric_results": result.metric_results,
        "drift_direction": result.drift_direction.value,
        "regression_status": result.regression_status.value,
        "warnings": result.warnings,
        "errors": result.errors
    }


def performance_review_result_to_dict(result: PerformanceReviewResult) -> Dict[str, Any]:
    return {
        "review_id": result.review_id,
        "created_at_utc": result.created_at_utc,
        "report_type": result.report_type.value,
        "status": result.status.value,
        "baselines": [performance_baseline_to_dict(b) for b in result.baselines],
        "samples": [current_performance_sample_to_dict(s) for s in result.samples],
        "comparisons": [baseline_comparison_result_to_dict(c) for c in result.comparisons],
        "threshold_results": result.threshold_results,  # List[Any] so assuming already serializable
        "regression_alerts": result.regression_alerts,  # List[Any] so assuming already serializable
        "acceptance_status": result.acceptance_status.value,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }
