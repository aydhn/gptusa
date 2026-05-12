from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
import uuid

from usa_signal_bot.core.enums import (
    PerformanceBaselineScope,
    PerformanceMetricName,
    SLAThresholdType,
    SLASeverity,
    BaselineComparisonStatus
)
from usa_signal_bot.core.exceptions import PerformanceBaselineValidationError


@dataclass
class SLAThreshold:
    threshold_id: str
    name: str
    scope: PerformanceBaselineScope
    metric_name: PerformanceMetricName
    threshold_type: SLAThresholdType
    warning_value: Union[float, str, None]
    critical_value: Union[float, str, None]
    blocker_value: Union[float, str, None]
    enabled: bool
    severity: SLASeverity
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SLAThresholdEvaluation:
    evaluation_id: str
    created_at_utc: str
    threshold_id: str
    scope: PerformanceBaselineScope
    metric_name: PerformanceMetricName
    observed_value: Union[float, str, None]
    baseline_value: Union[float, str, None]
    status: BaselineComparisonStatus
    severity: SLASeverity
    message: str
    evidence: Dict[str, Any]
    warnings: List[str]
    errors: List[str]


@dataclass
class SLAEvaluationReport:
    report_id: str
    created_at_utc: str
    scope: PerformanceBaselineScope
    status: BaselineComparisonStatus
    evaluations: List[SLAThresholdEvaluation]
    pass_count: int
    warn_count: int
    fail_count: int
    blocked_count: int
    warnings: List[str]
    errors: List[str]


def create_sla_threshold_id(scope: PerformanceBaselineScope, metric_name: PerformanceMetricName) -> str:
    return f"sla_thresh_{scope.value.lower()}_{metric_name.value.lower()}"


def create_sla_evaluation_id(prefix: str = "sla_eval") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def create_sla_report_id(prefix: str = "sla_report") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def validate_sla_threshold(threshold: SLAThreshold) -> None:
    if not threshold.name:
        raise PerformanceBaselineValidationError("SLAThreshold name cannot be empty.")

    # Optional logic enforcing blocker >= critical >= warning depending on threshold type could be here.
    if threshold.enabled:
        # Check if blocker is more loose than critical (simplified numeric check)
        if isinstance(threshold.blocker_value, (int, float)) and isinstance(threshold.critical_value, (int, float)):
            # Assuming max thresholds are typical
            if threshold.threshold_type in [SLAThresholdType.MAX, SLAThresholdType.DELTA_PCT, SLAThresholdType.DELTA_ABSOLUTE]:
                 if threshold.blocker_value < threshold.critical_value:
                     raise PerformanceBaselineValidationError("Blocker value cannot be less than critical value for MAX/DELTA thresholds.")

def validate_sla_evaluation_report(report: SLAEvaluationReport) -> None:
    if not report.report_id:
        raise PerformanceBaselineValidationError("report_id cannot be empty.")


def sla_threshold_to_dict(threshold: SLAThreshold) -> Dict[str, Any]:
    return {
        "threshold_id": threshold.threshold_id,
        "name": threshold.name,
        "scope": threshold.scope.value,
        "metric_name": threshold.metric_name.value,
        "threshold_type": threshold.threshold_type.value,
        "warning_value": threshold.warning_value,
        "critical_value": threshold.critical_value,
        "blocker_value": threshold.blocker_value,
        "enabled": threshold.enabled,
        "severity": threshold.severity.value,
        "description": threshold.description,
        "metadata": threshold.metadata
    }


def sla_threshold_evaluation_to_dict(evaluation: SLAThresholdEvaluation) -> Dict[str, Any]:
    return {
        "evaluation_id": evaluation.evaluation_id,
        "created_at_utc": evaluation.created_at_utc,
        "threshold_id": evaluation.threshold_id,
        "scope": evaluation.scope.value,
        "metric_name": evaluation.metric_name.value,
        "observed_value": evaluation.observed_value,
        "baseline_value": evaluation.baseline_value,
        "status": evaluation.status.value,
        "severity": evaluation.severity.value,
        "message": evaluation.message,
        "evidence": evaluation.evidence,
        "warnings": evaluation.warnings,
        "errors": evaluation.errors
    }


def sla_evaluation_report_to_dict(report: SLAEvaluationReport) -> Dict[str, Any]:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "scope": report.scope.value,
        "status": report.status.value,
        "evaluations": [sla_threshold_evaluation_to_dict(e) for e in report.evaluations],
        "pass_count": report.pass_count,
        "warn_count": report.warn_count,
        "fail_count": report.fail_count,
        "blocked_count": report.blocked_count,
        "warnings": report.warnings,
        "errors": report.errors
    }
