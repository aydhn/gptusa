from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import (
    ResourceProfileStatus,
    ResourceProfileScope,
    ResourceMetricName,
    CalibrationStatus,
    CalibrationDecision,
    ThrottlingAction,
    ThrottlingSeverity,
    ThrottlingReason,
    ProfilingReportType
)
from usa_signal_bot.core.exceptions import ProfilingValidationError

def create_resource_metric_id(prefix: str = "res_metric") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_resource_profile_id(prefix: str = "res_profile") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_budget_calibration_input_id(prefix: str = "cal_input") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_budget_calibration_id(prefix: str = "calibration") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_throttling_recommendation_id(prefix: str = "throttle_rec") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_throttling_plan_id(prefix: str = "throttle_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_profiling_review_id(prefix: str = "profiling_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

@dataclass
class ResourceMetric:
    metric_id: str
    name: ResourceMetricName
    value: int | float | str | None
    unit: str | None
    status: ResourceProfileStatus
    source: str
    created_at_utc: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ResourceProfile:
    profile_id: str
    scope: ResourceProfileScope
    target_name: str
    status: ResourceProfileStatus
    started_at_utc: str | None
    completed_at_utc: str | None
    wall_time_seconds: float | None
    process_time_seconds: float | None
    memory_current_bytes: int | None
    memory_peak_bytes: int | None
    artifact_size_bytes: int | None
    artifact_file_count: int | None
    output_growth_bytes: int | None
    output_growth_files: int | None
    metrics: list[ResourceMetric]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BudgetCalibrationInput:
    input_id: str
    created_at_utc: str
    scope: ResourceProfileScope
    profiles: list[ResourceProfile]
    current_budget: dict[str, Any]
    warnings: list[str]
    errors: list[str]

@dataclass
class BudgetCalibrationResult:
    calibration_id: str
    created_at_utc: str
    status: CalibrationStatus
    scope: ResourceProfileScope
    sample_count: int
    decision: CalibrationDecision
    current_budget: dict[str, Any]
    recommended_budget: dict[str, Any]
    confidence: float | None
    evidence: dict[str, Any]
    warnings: list[str]
    errors: list[str]

@dataclass
class ThrottlingRecommendation:
    recommendation_id: str
    task_id: str | None
    scope: ResourceProfileScope
    action: ThrottlingAction
    severity: ThrottlingSeverity
    reasons: list[ThrottlingReason]
    message: str
    suggested_changes: dict[str, Any]
    evidence: dict[str, Any]
    warnings: list[str] = field(default_factory=list)

@dataclass
class ThrottlingPlan:
    plan_id: str
    created_at_utc: str
    status: ResourceProfileStatus
    recommendations: list[ThrottlingRecommendation]
    blocked_count: int
    warning_count: int
    review_count: int
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

@dataclass
class ProfilingReviewResult:
    review_id: str
    created_at_utc: str
    report_type: ProfilingReportType
    status: ResourceProfileStatus
    profiles: list[ResourceProfile]
    calibration_results: list[BudgetCalibrationResult]
    throttling_plan: ThrottlingPlan | None
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def resource_metric_to_dict(metric: ResourceMetric) -> dict:
    return {
        "metric_id": metric.metric_id,
        "name": metric.name.value,
        "value": metric.value,
        "unit": metric.unit,
        "status": metric.status.value,
        "source": metric.source,
        "created_at_utc": metric.created_at_utc,
        "metadata": metric.metadata
    }

def resource_profile_to_dict(profile: ResourceProfile) -> dict:
    return {
        "profile_id": profile.profile_id,
        "scope": profile.scope.value,
        "target_name": profile.target_name,
        "status": profile.status.value,
        "started_at_utc": profile.started_at_utc,
        "completed_at_utc": profile.completed_at_utc,
        "wall_time_seconds": profile.wall_time_seconds,
        "process_time_seconds": profile.process_time_seconds,
        "memory_current_bytes": profile.memory_current_bytes,
        "memory_peak_bytes": profile.memory_peak_bytes,
        "artifact_size_bytes": profile.artifact_size_bytes,
        "artifact_file_count": profile.artifact_file_count,
        "output_growth_bytes": profile.output_growth_bytes,
        "output_growth_files": profile.output_growth_files,
        "metrics": [resource_metric_to_dict(m) for m in profile.metrics],
        "warnings": profile.warnings,
        "errors": profile.errors,
        "metadata": profile.metadata
    }

def budget_calibration_input_to_dict(payload: BudgetCalibrationInput) -> dict:
    return {
        "input_id": payload.input_id,
        "created_at_utc": payload.created_at_utc,
        "scope": payload.scope.value,
        "profiles": [resource_profile_to_dict(p) for p in payload.profiles],
        "current_budget": payload.current_budget,
        "warnings": payload.warnings,
        "errors": payload.errors
    }

def budget_calibration_result_to_dict(result: BudgetCalibrationResult) -> dict:
    return {
        "calibration_id": result.calibration_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "scope": result.scope.value,
        "sample_count": result.sample_count,
        "decision": result.decision.value,
        "current_budget": result.current_budget,
        "recommended_budget": result.recommended_budget,
        "confidence": result.confidence,
        "evidence": result.evidence,
        "warnings": result.warnings,
        "errors": result.errors
    }

def throttling_recommendation_to_dict(rec: ThrottlingRecommendation) -> dict:
    return {
        "recommendation_id": rec.recommendation_id,
        "task_id": rec.task_id,
        "scope": rec.scope.value,
        "action": rec.action.value,
        "severity": rec.severity.value,
        "reasons": [r.value for r in rec.reasons],
        "message": rec.message,
        "suggested_changes": rec.suggested_changes,
        "evidence": rec.evidence,
        "warnings": rec.warnings
    }

def throttling_plan_to_dict(plan: ThrottlingPlan) -> dict:
    return {
        "plan_id": plan.plan_id,
        "created_at_utc": plan.created_at_utc,
        "status": plan.status.value,
        "recommendations": [throttling_recommendation_to_dict(r) for r in plan.recommendations],
        "blocked_count": plan.blocked_count,
        "warning_count": plan.warning_count,
        "review_count": plan.review_count,
        "output_paths": plan.output_paths,
        "warnings": plan.warnings,
        "errors": plan.errors
    }

def profiling_review_result_to_dict(result: ProfilingReviewResult) -> dict:
    return {
        "review_id": result.review_id,
        "created_at_utc": result.created_at_utc,
        "report_type": result.report_type.value,
        "status": result.status.value,
        "profiles": [resource_profile_to_dict(p) for p in result.profiles],
        "calibration_results": [budget_calibration_result_to_dict(c) for c in result.calibration_results],
        "throttling_plan": throttling_plan_to_dict(result.throttling_plan) if result.throttling_plan else None,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

def validate_resource_metric(metric: ResourceMetric) -> None:
    if isinstance(metric.value, (int, float)):
        if "time" in metric.name.value.lower() and metric.value < 0:
            raise ProfilingValidationError(f"Negative duration in metric: {metric.name}")
        if "bytes" in metric.name.value.lower() and metric.value < 0:
            raise ProfilingValidationError(f"Negative bytes in metric: {metric.name}")
        if "size" in metric.name.value.lower() and metric.value < 0:
            raise ProfilingValidationError(f"Negative size in metric: {metric.name}")

def validate_resource_profile(profile: ResourceProfile) -> None:
    if profile.wall_time_seconds is not None and profile.wall_time_seconds < 0:
        raise ProfilingValidationError("Negative wall_time_seconds")
    if profile.process_time_seconds is not None and profile.process_time_seconds < 0:
        raise ProfilingValidationError("Negative process_time_seconds")
    if profile.memory_current_bytes is not None and profile.memory_current_bytes < 0:
        raise ProfilingValidationError("Negative memory_current_bytes")
    if profile.memory_peak_bytes is not None and profile.memory_peak_bytes < 0:
        raise ProfilingValidationError("Negative memory_peak_bytes")
    if profile.artifact_size_bytes is not None and profile.artifact_size_bytes < 0:
        raise ProfilingValidationError("Negative artifact_size_bytes")

    for m in profile.metrics:
        validate_resource_metric(m)

def validate_budget_calibration_result(result: BudgetCalibrationResult) -> None:
    if result.confidence is not None and not (0 <= result.confidence <= 1):
        raise ProfilingValidationError("Confidence must be between 0 and 1")
    if result.sample_count < 0:
        raise ProfilingValidationError("Sample count cannot be negative")

def validate_throttling_plan(plan: ThrottlingPlan) -> None:
    for rec in plan.recommendations:
        if not rec.message:
            raise ProfilingValidationError("Recommendation message cannot be empty")

        lower_msg = rec.message.lower()
        if "investment advice" in lower_msg or "live approval" in lower_msg:
            raise ProfilingValidationError("Profiling output cannot contain investment advice language")
