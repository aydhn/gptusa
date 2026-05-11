import json
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.profiling.profiling_models import (
    ResourceProfile,
    BudgetCalibrationResult,
    ThrottlingPlan,
    ProfilingReviewResult,
    resource_profile_to_dict,
    budget_calibration_result_to_dict,
    throttling_plan_to_dict,
    profiling_review_result_to_dict
)
from usa_signal_bot.core.exceptions import ProfilingValidationError

@dataclass
class ProfilingValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProfilingValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ProfilingValidationIssue]
    warnings: list[str]
    errors: list[str]

def _check_sensitive_fields(payload: dict[str, Any], issues: list[ProfilingValidationIssue]) -> None:
    text = json.dumps(payload).lower()

    forbidden_keys = ["external_endpoint", "telemetry_url", "prometheus", "sentry", "datadog", "opentelemetry"]
    for k in forbidden_keys:
        if k in text:
            issues.append(ProfilingValidationIssue("BLOCK", "payload", f"External telemetry field detected: {k}"))

    secret_keys = ["api_key", "secret", "password"]
    if "api_key" in text and "***redacted***" not in text:
         issues.append(ProfilingValidationIssue("BLOCK", "payload", "Unredacted secret/api_key detected."))

def _check_live_language(text: str, issues: list[ProfilingValidationIssue]) -> None:
    lower_text = text.lower()
    forbidden = ["live approved", "sent to broker", "kesin al", "garanti", "investment advice", "optimal portfolio"]
    for f in forbidden:
        if f in lower_text:
            issues.append(ProfilingValidationIssue("BLOCK", "text", f"Forbidden language detected: {f}"))

def _build_report(issues: list[ProfilingValidationIssue]) -> ProfilingValidationReport:
    warns = [i.message for i in issues if i.severity == "WARNING"]
    errs = [i.message for i in issues if i.severity == "ERROR"]
    blocks = [i.message for i in issues if i.severity == "BLOCK"]

    return ProfilingValidationReport(
        valid=len(errs) == 0 and len(blocks) == 0,
        issue_count=len(issues),
        warning_count=len(warns),
        error_count=len(errs),
        blocked_count=len(blocks),
        issues=issues,
        warnings=warns,
        errors=errs + blocks
    )

def validate_resource_profile_report(profile: ResourceProfile) -> ProfilingValidationReport:
    issues = []

    if profile.wall_time_seconds is not None and profile.wall_time_seconds < 0:
        issues.append(ProfilingValidationIssue("ERROR", "wall_time_seconds", "Negative duration"))

    if profile.memory_peak_bytes is not None and profile.memory_peak_bytes < 0:
        issues.append(ProfilingValidationIssue("ERROR", "memory_peak_bytes", "Negative memory"))

    payload = resource_profile_to_dict(profile)
    _check_sensitive_fields(payload, issues)

    return _build_report(issues)

def validate_budget_calibration_result_report(result: BudgetCalibrationResult) -> ProfilingValidationReport:
    issues = []
    payload = budget_calibration_result_to_dict(result)
    _check_sensitive_fields(payload, issues)
    return _build_report(issues)

def validate_throttling_plan_report(plan: ThrottlingPlan) -> ProfilingValidationReport:
    issues = []
    payload = throttling_plan_to_dict(plan)

    _check_sensitive_fields(payload, issues)
    _check_live_language(json.dumps(payload), issues)

    return _build_report(issues)

def validate_profiling_review_result_report(result: ProfilingReviewResult) -> ProfilingValidationReport:
    issues = []
    payload = profiling_review_result_to_dict(result)

    _check_sensitive_fields(payload, issues)
    _check_live_language(json.dumps(payload), issues)

    return _build_report(issues)

def validate_no_sensitive_data_in_profiling_payload(payload: dict[str, Any]) -> ProfilingValidationReport:
    issues = []
    _check_sensitive_fields(payload, issues)
    return _build_report(issues)

def validate_no_live_execution_language_in_profiling(text: str) -> ProfilingValidationReport:
    issues = []
    _check_live_language(text, issues)
    return _build_report(issues)

def validate_no_external_telemetry_fields(payload: dict[str, Any]) -> ProfilingValidationReport:
    issues = []
    _check_sensitive_fields(payload, issues)
    return _build_report(issues)

def profiling_validation_report_to_text(report: ProfilingValidationReport) -> str:
    status = "VALID" if report.valid else "INVALID"
    lines = [
        f"Validation Report: {status}",
        f"  Issues: {report.issue_count}",
        f"  Blocked: {report.blocked_count}"
    ]
    for i in report.issues:
        lines.append(f"  - [{i.severity}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_profiling_valid(report: ProfilingValidationReport) -> None:
    if not report.valid:
        raise ProfilingValidationError(f"Profiling validation failed: {report.errors}")
