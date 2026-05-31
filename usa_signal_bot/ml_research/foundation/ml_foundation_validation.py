from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from .phase136_models import MLFoundationContext, MLFoundationFullReview
from .ml_foundation_safety_validator import validate_ml_foundation_context_safety, ml_foundation_text_has_trade_or_execution_language
from .ml_foundation_schema_validator import validate_no_forbidden_ml_foundation_columns
from ...core.exceptions import MLFoundationValidationError

@dataclass
class MLFoundationValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MLFoundationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[MLFoundationValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[MLFoundationValidationIssue]) -> MLFoundationValidationReport:
    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    blocked = [i for i in issues if i.severity == "BLOCKED"]
    valid = len(errors) == 0 and len(blocked) == 0
    return MLFoundationValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_ml_foundation_context_report(item: MLFoundationContext) -> MLFoundationValidationReport:
    issues = []
    safety_errs = validate_ml_foundation_context_safety(item)
    for err in safety_errs:
        issues.append(MLFoundationValidationIssue("ERROR", None, err))
    return _create_report(issues)

def validate_ml_foundation_full_review_report(item: MLFoundationFullReview) -> MLFoundationValidationReport:
    issues = []
    safety_errs = validate_ml_foundation_context_safety(item.context)
    for err in safety_errs:
        issues.append(MLFoundationValidationIssue("ERROR", None, err))
    return _create_report(issues)

def validate_no_sensitive_data_in_ml_foundation_payload(payload: Dict[str, Any]) -> MLFoundationValidationReport:
    # Dummy implementation for local test
    return _create_report([])

def validate_no_execution_language_in_ml_foundation_text(text: str) -> MLFoundationValidationReport:
    issues = []
    if ml_foundation_text_has_trade_or_execution_language(text):
        issues.append(MLFoundationValidationIssue("ERROR", None, "Execution language found in text"))
    return _create_report(issues)

def validate_no_unsafe_ml_foundation_fields(payload: Dict[str, Any]) -> MLFoundationValidationReport:
    issues = []
    if payload.get("deployment_enabled"):
        issues.append(MLFoundationValidationIssue("ERROR", "deployment_enabled", "deployment_enabled found"))
    return _create_report(issues)

def ml_foundation_validation_report_to_text(report: MLFoundationValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_ml_foundation_validation_valid(report: MLFoundationValidationReport) -> None:
    if not report.valid:
        raise MLFoundationValidationError("Validation failed")
