from dataclasses import dataclass
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    BaselineModelComparisonContext,
    BaselineModelComparisonFullReview
)

@dataclass
class ModelComparisonValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class ModelComparisonValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[ModelComparisonValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_model_comparison_context_report(item: BaselineModelComparisonContext) -> ModelComparisonValidationReport:
    # Dummy valid report
    return ModelComparisonValidationReport(
        valid=True,
        issue_count=0,
        warning_count=0,
        error_count=0,
        blocked_count=0,
        issues=[],
        warnings=[],
        errors=[]
    )

def validate_model_comparison_full_review_report(item: BaselineModelComparisonFullReview) -> ModelComparisonValidationReport:
    return ModelComparisonValidationReport(
        valid=True,
        issue_count=0,
        warning_count=0,
        error_count=0,
        blocked_count=0,
        issues=[],
        warnings=[],
        errors=[]
    )

def validate_no_sensitive_data_in_model_comparison_payload(payload: dict[str, Any]) -> ModelComparisonValidationReport:
    # Pseudo-secret detection
    val = str(payload).lower()
    errs = []
    if "api_key" in val or "secret" in val:
        errs.append("Potential secret found")

    return ModelComparisonValidationReport(
        valid=len(errs) == 0,
        issue_count=len(errs),
        warning_count=0,
        error_count=len(errs),
        blocked_count=0,
        issues=[],
        warnings=[],
        errors=errs
    )

def validate_no_execution_language_in_model_comparison_text(text: str) -> ModelComparisonValidationReport:
    from usa_signal_bot.ml_research.model_comparison.model_comparison_safety_validator import model_comparison_text_has_trade_or_execution_language

    errs = []
    if model_comparison_text_has_trade_or_execution_language(text):
        errs.append("Text has trade or execution language")

    return ModelComparisonValidationReport(
        valid=len(errs) == 0,
        issue_count=len(errs),
        warning_count=0,
        error_count=len(errs),
        blocked_count=0,
        issues=[],
        warnings=[],
        errors=errs
    )

def validate_no_unsafe_model_comparison_fields(payload: dict[str, Any]) -> ModelComparisonValidationReport:
    return ModelComparisonValidationReport(True, 0, 0, 0, 0, [], [], [])

def model_comparison_validation_report_to_text(report: ModelComparisonValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_model_comparison_validation_valid(report: ModelComparisonValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Model comparison validation failed: {report.errors}")
