from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from usa_signal_bot.release.phase159_models import AdvancedAcceptanceContext, AdvancedAcceptanceFullReview
from usa_signal_bot.release.advanced_acceptance_safety_validator import (
    validate_advanced_acceptance_context_safety,
    advanced_acceptance_text_has_trade_or_execution_language,
    advanced_acceptance_payload_has_forbidden_fields
)
from usa_signal_bot.release.advanced_acceptance_schema_validator import validate_advanced_acceptance_context_schema

@dataclass
class AdvancedAcceptanceValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any]

@dataclass
class AdvancedAcceptanceValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[AdvancedAcceptanceValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_advanced_acceptance_context_report(item: AdvancedAcceptanceContext) -> AdvancedAcceptanceValidationReport:
    schema_errors = validate_advanced_acceptance_context_schema(item)
    safety_errors = validate_advanced_acceptance_context_safety(item)

    issues = []
    for e in schema_errors:
        issues.append(AdvancedAcceptanceValidationIssue(severity="error", field=None, message=e, details={}))
    for e in safety_errors:
        issues.append(AdvancedAcceptanceValidationIssue(severity="blocked", field=None, message=e, details={}))

    errors = schema_errors + safety_errors
    return AdvancedAcceptanceValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(schema_errors),
        blocked_count=len(safety_errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_advanced_acceptance_full_review_report(item: AdvancedAcceptanceFullReview) -> AdvancedAcceptanceValidationReport:
    return validate_advanced_acceptance_context_report(item.context)

def validate_no_sensitive_data_in_advanced_acceptance_payload(payload: Dict[str, Any]) -> AdvancedAcceptanceValidationReport:
    # A simplified mock
    issues = []
    if "api_key" in str(payload).lower() or "secret" in str(payload).lower():
         issues.append(AdvancedAcceptanceValidationIssue(severity="blocked", field=None, message="Sensitive data leak risk", details={}))

    return AdvancedAcceptanceValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=["Sensitive data leak risk"] if issues else []
    )

def validate_no_execution_language_in_advanced_acceptance_text(text: str) -> AdvancedAcceptanceValidationReport:
    has_exec = advanced_acceptance_text_has_trade_or_execution_language(text)
    issues = []
    if has_exec:
        issues.append(AdvancedAcceptanceValidationIssue(severity="blocked", field=None, message="Execution language detected", details={}))

    return AdvancedAcceptanceValidationReport(
        valid=not has_exec,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=["Execution language detected"] if issues else []
    )

def validate_no_unsafe_advanced_acceptance_fields(payload: Dict[str, Any]) -> AdvancedAcceptanceValidationReport:
    has_unsafe = advanced_acceptance_payload_has_forbidden_fields(payload)
    issues = []
    if has_unsafe:
        issues.append(AdvancedAcceptanceValidationIssue(severity="blocked", field=None, message="Unsafe fields detected", details={}))

    return AdvancedAcceptanceValidationReport(
        valid=not has_unsafe,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=["Unsafe fields detected"] if issues else []
    )

def advanced_acceptance_validation_report_to_text(report: AdvancedAcceptanceValidationReport) -> str:
    lines = [f"Validation Report: {'Valid' if report.valid else 'Invalid'}"]
    for i in report.issues:
        lines.append(f" - [{i.severity.upper()}] {i.message}")
    return "\n".join(lines)

def assert_advanced_acceptance_validation_valid(report: AdvancedAcceptanceValidationReport) -> None:
    if not report.valid:
        from usa_signal_bot.core.exceptions import AdvancedAcceptanceValidationError
        raise AdvancedAcceptanceValidationError(f"Validation failed: {report.errors}")
