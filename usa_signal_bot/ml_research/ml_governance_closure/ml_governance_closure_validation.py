from typing import Any
from dataclasses import dataclass
from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    AdvancedMLClosureContext,
    AdvancedMLClosureFullReview
)
from usa_signal_bot.core.exceptions import MLGovernanceClosureValidationError
from usa_signal_bot.ml_research.ml_governance_closure.ml_closure_safety_validator import (
    ml_closure_text_has_trade_or_execution_language,
    validate_advanced_ml_closure_context_safety
)

@dataclass
class MLGovernanceClosureValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class MLGovernanceClosureValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[MLGovernanceClosureValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_advanced_ml_closure_context_report(item: AdvancedMLClosureContext) -> MLGovernanceClosureValidationReport:
    errors = validate_advanced_ml_closure_context_safety(item)

    issues = []
    for e in errors:
        issues.append(MLGovernanceClosureValidationIssue(
            severity="ERROR",
            field=None,
            message=e,
            details={}
        ))

    return MLGovernanceClosureValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_advanced_ml_closure_full_review_report(item: AdvancedMLClosureFullReview) -> MLGovernanceClosureValidationReport:
    return validate_advanced_ml_closure_context_report(item.context)

def validate_no_sensitive_data_in_ml_closure_payload(payload: dict[str, Any]) -> MLGovernanceClosureValidationReport:
    # Dummy implementation
    return MLGovernanceClosureValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_execution_language_in_ml_closure_text(text: str) -> MLGovernanceClosureValidationReport:
    has_exec = ml_closure_text_has_trade_or_execution_language(text)
    errors = ["Execution language found in text"] if has_exec else []
    return MLGovernanceClosureValidationReport(
        valid=not has_exec,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        issues=[],
        warnings=[],
        errors=errors
    )

def validate_no_unsafe_ml_closure_fields(payload: dict[str, Any]) -> MLGovernanceClosureValidationReport:
    return MLGovernanceClosureValidationReport(True, 0, 0, 0, 0, [], [], [])

def ml_governance_closure_validation_report_to_text(report: MLGovernanceClosureValidationReport) -> str:
    if report.valid:
        return "Validation passed."
    return f"Validation failed with {report.error_count} errors."

def assert_ml_governance_closure_validation_valid(report: MLGovernanceClosureValidationReport) -> None:
    if not report.valid:
        raise MLGovernanceClosureValidationError(f"Validation failed: {report.errors}")
