from dataclasses import dataclass, field
from typing import Any, List, Optional
import re
from usa_signal_bot.core.exceptions import LifecycleValidationError
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    StartupCheckReport,
    ServiceReadinessMatrix,
    ReadinessGate,
    RuntimeLifecycleContext,
    RuntimeLifecycleFullReview
)

@dataclass
class RuntimeLifecycleValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict

@dataclass
class RuntimeLifecycleValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[RuntimeLifecycleValidationIssue]
    warnings: List[str]
    errors: List[str]

def _check_boolean_field(obj: Any, field_name: str, expected: bool, severity: str, issues: List[RuntimeLifecycleValidationIssue]):
    val = getattr(obj, field_name, None)
    if val is not expected:
        issues.append(RuntimeLifecycleValidationIssue(
            severity=severity,
            field=field_name,
            message=f"{field_name} MUST be {expected}, but was {val}",
            details={"actual": val, "expected": expected}
        ))

def validate_startup_check_report_payload(report: StartupCheckReport) -> RuntimeLifecycleValidationReport:
    issues = []
    _check_boolean_field(report, "execution_performed", False, "error", issues)
    _check_boolean_field(report, "network_used", False, "error", issues)
    _check_boolean_field(report, "broker_used", False, "error", issues)
    _check_boolean_field(report, "order_created", False, "error", issues)
    _check_boolean_field(report, "paper_state_mutated", False, "error", issues)
    _check_boolean_field(report, "telegram_real_sent", False, "error", issues)
    _check_boolean_field(report, "scraping_used", False, "error", issues)
    _check_boolean_field(report, "dashboard_started", False, "error", issues)
    _check_boolean_field(report, "startup_checks_metadata_only", True, "error", issues)

    valid = len([i for i in issues if i.severity == "error"]) == 0
    return RuntimeLifecycleValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=len([i for i in issues if i.severity == "warning"]),
        error_count=len([i for i in issues if i.severity == "error"]),
        blocked_count=0,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "warning"],
        errors=[i.message for i in issues if i.severity == "error"]
    )

def validate_service_readiness_matrix_payload(matrix: ServiceReadinessMatrix) -> RuntimeLifecycleValidationReport:
    issues = []
    if matrix.all_required_services_ready and not matrix.no_execution_ready:
        issues.append(RuntimeLifecycleValidationIssue(
            severity="error",
            field="no_execution_ready",
            message="Matrix claims services are ready, but no_execution_ready is False",
            details={}
        ))
    valid = len([i for i in issues if i.severity == "error"]) == 0
    return RuntimeLifecycleValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=len([i for i in issues if i.severity == "warning"]),
        error_count=len([i for i in issues if i.severity == "error"]),
        blocked_count=0,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "warning"],
        errors=[i.message for i in issues if i.severity == "error"]
    )

def validate_readiness_gate_payload(gate: ReadinessGate) -> RuntimeLifecycleValidationReport:
    issues = []
    for field in ["activation_allowed", "active_paper_enabled", "broker_execution_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled", "dashboard_enabled", "execution_performed", "network_used", "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent", "scraping_used", "dashboard_started"]:
        _check_boolean_field(gate, field, False, "error", issues)
    _check_boolean_field(gate, "metadata_only", True, "error", issues)

    valid = len([i for i in issues if i.severity == "error"]) == 0
    return RuntimeLifecycleValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=len([i for i in issues if i.severity == "warning"]),
        error_count=len([i for i in issues if i.severity == "error"]),
        blocked_count=0,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "warning"],
        errors=[i.message for i in issues if i.severity == "error"]
    )

def validate_runtime_lifecycle_context_payload(context: RuntimeLifecycleContext) -> RuntimeLifecycleValidationReport:
    issues = []
    for field in ["activation_allowed", "active_paper_enabled", "broker_execution_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled", "dashboard_enabled", "execution_performed", "network_used", "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent", "scraping_used", "dashboard_started"]:
        _check_boolean_field(context, field, False, "error", issues)

    valid = len([i for i in issues if i.severity == "error"]) == 0
    return RuntimeLifecycleValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=len([i for i in issues if i.severity == "warning"]),
        error_count=len([i for i in issues if i.severity == "error"]),
        blocked_count=0,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "warning"],
        errors=[i.message for i in issues if i.severity == "error"]
    )

def validate_runtime_lifecycle_full_review_report(review: RuntimeLifecycleFullReview) -> RuntimeLifecycleValidationReport:
    all_issues = []

    if review.startup_report:
        r1 = validate_startup_check_report_payload(review.startup_report)
        all_issues.extend(r1.issues)
    if review.readiness_matrix:
        r2 = validate_service_readiness_matrix_payload(review.readiness_matrix)
        all_issues.extend(r2.issues)
    if review.readiness_gate:
        r3 = validate_readiness_gate_payload(review.readiness_gate)
        all_issues.extend(r3.issues)
    if review.lifecycle_context:
        r4 = validate_runtime_lifecycle_context_payload(review.lifecycle_context)
        all_issues.extend(r4.issues)

    valid = len([i for i in all_issues if i.severity == "error"]) == 0
    return RuntimeLifecycleValidationReport(
        valid=valid,
        issue_count=len(all_issues),
        warning_count=len([i for i in all_issues if i.severity == "warning"]),
        error_count=len([i for i in all_issues if i.severity == "error"]),
        blocked_count=0,
        issues=all_issues,
        warnings=[i.message for i in all_issues if i.severity == "warning"],
        errors=[i.message for i in all_issues if i.severity == "error"]
    )

def validate_no_sensitive_data_in_lifecycle_payload(payload: dict) -> RuntimeLifecycleValidationReport:
    issues = []
    payload_str = str(payload).lower()
    for sensitive in ["api_key", "token", "secret", "password", "broker_order_id", "live_order_id", "sent_to_broker"]:
        if sensitive in payload_str:
            issues.append(RuntimeLifecycleValidationIssue("error", None, f"Sensitive data detected: {sensitive}", {}))

    valid = len([i for i in issues if i.severity == "error"]) == 0
    return RuntimeLifecycleValidationReport(
        valid=valid, issue_count=len(issues), warning_count=0, error_count=len(issues), blocked_count=0,
        issues=issues, warnings=[], errors=[i.message for i in issues if i.severity == "error"]
    )

def validate_no_execution_language_in_lifecycle_text(text: str) -> RuntimeLifecycleValidationReport:
    issues = []
    text_lower = text.lower()
    forbidden = ["emir gönderildi", "aktif trading başladı", "paper'a alındı", "kesin al", "garanti kâr"]
    for phrase in forbidden:
        if phrase in text_lower:
            issues.append(RuntimeLifecycleValidationIssue("error", None, f"Execution language detected: {phrase}", {}))

    valid = len([i for i in issues if i.severity == "error"]) == 0
    return RuntimeLifecycleValidationReport(
        valid=valid, issue_count=len(issues), warning_count=0, error_count=len(issues), blocked_count=0,
        issues=issues, warnings=[], errors=[i.message for i in issues if i.severity == "error"]
    )

def runtime_lifecycle_validation_report_to_text(report: RuntimeLifecycleValidationReport) -> str:
    lines = [
        "=== RUNTIME LIFECYCLE VALIDATION REPORT ===",
        f"Valid: {report.valid}",
        f"Errors: {report.error_count}",
        f"Warnings: {report.warning_count}"
    ]
    if report.errors:
        lines.append("\nErrors:")
        for err in report.errors:
            lines.append(f"- {err}")
    if report.warnings:
        lines.append("\nWarnings:")
        for warn in report.warnings:
            lines.append(f"- {warn}")
    return "\n".join(lines)

def assert_runtime_lifecycle_valid(report: RuntimeLifecycleValidationReport) -> None:
    if not report.valid:
        raise LifecycleValidationError(f"Runtime lifecycle validation failed with {report.error_count} errors: {', '.join(report.errors)}")
