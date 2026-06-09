from typing import List, Dict, Any
from dataclasses import dataclass, field
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalClosureContext,
    FinalClosureFullReview
)
from usa_signal_bot.release.final_closure.final_closure_safety_validator import (
    validate_final_closure_context_safety,
    final_closure_text_has_trade_or_execution_language,
    final_closure_payload_has_forbidden_fields
)
from usa_signal_bot.release.final_closure.final_closure_schema_validator import (
    validate_final_closure_context_schema
)
from usa_signal_bot.core.exceptions import FinalClosureValidationError

@dataclass
class FinalClosureValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalClosureValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[FinalClosureValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_final_closure_context_report(item: FinalClosureContext) -> FinalClosureValidationReport:
    issues = []
    errors = []

    schema_errs = validate_final_closure_context_schema(item)
    for err in schema_errs:
        issues.append(FinalClosureValidationIssue("ERROR", None, err))
        errors.append(err)

    safety_errs = validate_final_closure_context_safety(item)
    for err in safety_errs:
        issues.append(FinalClosureValidationIssue("ERROR", None, err))
        errors.append(err)

    valid = len(errors) == 0

    return FinalClosureValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=issues,
        warnings=[],
        errors=errors
    )

def validate_final_closure_full_review_report(item: FinalClosureFullReview) -> FinalClosureValidationReport:
    return validate_final_closure_context_report(item.context)

def validate_no_sensitive_data_in_final_closure_payload(payload: Dict[str, Any]) -> FinalClosureValidationReport:
    import json
    payload_str = json.dumps(payload).lower()
    sensitive = ["password", "secret", "token", "api_key"]

    errors = []
    for s in sensitive:
        if f'"{s}"' in payload_str or f"'{s}'" in payload_str:
            errors.append(f"Potentially sensitive data found matching '{s}'")

    return FinalClosureValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=[FinalClosureValidationIssue("ERROR", None, err) for err in errors],
        warnings=[],
        errors=errors
    )

def validate_no_execution_language_in_final_closure_text(text: str) -> FinalClosureValidationReport:
    has_language = final_closure_text_has_trade_or_execution_language(text)
    errors = ["Execution language found in text"] if has_language else []

    return FinalClosureValidationReport(
        valid=not has_language,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=[FinalClosureValidationIssue("ERROR", None, err) for err in errors],
        warnings=[],
        errors=errors
    )

def validate_no_unsafe_final_closure_fields(payload: Dict[str, Any]) -> FinalClosureValidationReport:
    has_forbidden = final_closure_payload_has_forbidden_fields(payload)
    errors = ["Forbidden fields found in payload"] if has_forbidden else []

    return FinalClosureValidationReport(
        valid=not has_forbidden,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=[FinalClosureValidationIssue("ERROR", None, err) for err in errors],
        warnings=[],
        errors=errors
    )

def final_closure_validation_report_to_text(report: FinalClosureValidationReport) -> str:
    return f"Validation Report: Valid={report.valid}, Errors={report.error_count}"

def assert_final_closure_validation_valid(report: FinalClosureValidationReport) -> None:
    if not report.valid:
        raise FinalClosureValidationError(f"Validation failed: {report.errors}")
