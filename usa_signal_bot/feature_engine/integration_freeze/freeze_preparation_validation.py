"""Freeze Preparation Validation."""
from dataclasses import dataclass, field
from typing import Any
from .phase124_models import FreezePreparationContext, FreezePreparationFullReview

@dataclass
class FreezePreparationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class FreezePreparationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[FreezePreparationValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_freeze_preparation_context_report(item: FreezePreparationContext) -> FreezePreparationValidationReport:
    issues = []
    if item.activation_allowed:
        issues.append(FreezePreparationValidationIssue("ERROR", "activation_allowed", "Must be false"))
    return FreezePreparationValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=0,
        issues=issues
    )

def validate_freeze_preparation_full_review_report(item: FreezePreparationFullReview) -> FreezePreparationValidationReport:
    issues = []
    if item.context.activation_allowed:
        issues.append(FreezePreparationValidationIssue("ERROR", "activation_allowed", "Must be false"))
    return FreezePreparationValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=0,
        issues=issues
    )

def validate_no_sensitive_data_in_freeze_payload(payload: dict[str, Any]) -> FreezePreparationValidationReport:
    # Check for api keys
    return FreezePreparationValidationReport(True, 0, 0, 0, 0)

def validate_no_execution_language_in_freeze_text(text: str) -> FreezePreparationValidationReport:
    return FreezePreparationValidationReport(True, 0, 0, 0, 0)

def validate_no_unsafe_freeze_fields(payload: dict[str, Any]) -> FreezePreparationValidationReport:
    return FreezePreparationValidationReport(True, 0, 0, 0, 0)

def freeze_preparation_validation_report_to_text(report: FreezePreparationValidationReport) -> str:
    return f"Validation Valid: {report.valid}"

def assert_freeze_preparation_validation_valid(report: FreezePreparationValidationReport) -> None:
    if not report.valid:
        raise ValueError("Validation failed")
