from dataclasses import dataclass
from typing import Any
from usa_signal_bot.regime_classification.validation.phase132_models import (
    RegimeContextValidationContext,
    RegimeContextValidationFullReview
)
from usa_signal_bot.regime_classification.validation.compatibility_validation_safety_validator import (
    validate_regime_context_validation_context_safety,
    context_validation_text_has_trade_or_execution_language
)
from usa_signal_bot.regime_classification.validation.compatibility_validation_schema_validator import validate_no_forbidden_context_validation_columns

@dataclass
class RegimeContextValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class RegimeContextValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[RegimeContextValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_regime_context_validation_context_report(item: RegimeContextValidationContext) -> RegimeContextValidationReport:
    errors = validate_regime_context_validation_context_safety(item)
    issues = [RegimeContextValidationIssue("ERROR", None, e, {}) for e in errors]
    return RegimeContextValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_regime_context_validation_full_review_report(item: RegimeContextValidationFullReview) -> RegimeContextValidationReport:
    return validate_regime_context_validation_context_report(item.context)

def validate_no_sensitive_data_in_context_validation_payload(payload: dict[str, Any]) -> RegimeContextValidationReport:
    errors = []
    # simplified mock
    issues = [RegimeContextValidationIssue("ERROR", None, e, {}) for e in errors]
    return RegimeContextValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_execution_language_in_context_validation_text(text: str) -> RegimeContextValidationReport:
    errors = []
    if context_validation_text_has_trade_or_execution_language(text):
        errors.append("Execution language found")
    issues = [RegimeContextValidationIssue("ERROR", None, e, {}) for e in errors]
    return RegimeContextValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_no_unsafe_context_validation_fields(payload: dict[str, Any]) -> RegimeContextValidationReport:
    errors = validate_no_forbidden_context_validation_columns(list(payload.keys()))
    issues = [RegimeContextValidationIssue("ERROR", None, e, {}) for e in errors]
    return RegimeContextValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def regime_context_validation_report_to_text(report: RegimeContextValidationReport) -> str:
    return f"Report valid: {report.valid}. Errors: {report.error_count}"

def assert_regime_context_validation_valid(report: RegimeContextValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Regime context validation failed: {report.errors}")
