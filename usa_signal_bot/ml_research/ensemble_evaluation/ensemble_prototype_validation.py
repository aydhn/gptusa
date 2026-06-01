from dataclasses import dataclass
from typing import Any, Dict, List

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeContext,
    EnsemblePrototypeFullReview
)
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_schema_validator import FORBIDDEN_FRAGMENTS

@dataclass
class EnsemblePrototypeValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any]

@dataclass
class EnsemblePrototypeValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[EnsemblePrototypeValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_ensemble_prototype_context_report(item: EnsemblePrototypeContext) -> EnsemblePrototypeValidationReport:
    return validate_no_sensitive_data_in_ensemble_prototype_payload({"context_id": item.context_id})

def validate_ensemble_prototype_full_review_report(item: EnsemblePrototypeFullReview) -> EnsemblePrototypeValidationReport:
    return validate_no_sensitive_data_in_ensemble_prototype_payload({"review_id": item.review_id})

def validate_no_sensitive_data_in_ensemble_prototype_payload(payload: Dict[str, Any]) -> EnsemblePrototypeValidationReport:
    # simple mock
    return EnsemblePrototypeValidationReport(
        valid=True,
        issue_count=0,
        warning_count=0,
        error_count=0,
        blocked_count=0,
        issues=[],
        warnings=[],
        errors=[]
    )

def validate_no_execution_language_in_ensemble_prototype_text(text: str) -> EnsemblePrototypeValidationReport:
    t = text.lower()
    errors = []
    for f in FORBIDDEN_FRAGMENTS:
        if f in t:
            errors.append(f"Forbidden: {f}")
    return EnsemblePrototypeValidationReport(
        valid=len(errors)==0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=[EnsemblePrototypeValidationIssue("ERROR", None, e, {}) for e in errors],
        warnings=[],
        errors=errors
    )

def validate_no_unsafe_ensemble_prototype_fields(payload: Dict[str, Any]) -> EnsemblePrototypeValidationReport:
    return validate_no_sensitive_data_in_ensemble_prototype_payload(payload)

def ensemble_prototype_validation_report_to_text(report: EnsemblePrototypeValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_ensemble_prototype_validation_valid(report: EnsemblePrototypeValidationReport) -> None:
    if not report.valid:
        raise ValueError("Validation failed: " + str(report.errors))
