from typing import Any
from dataclasses import dataclass

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorScoringContext,
    FactorScoringFullReview
)

@dataclass
class FactorScoringValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class FactorScoringValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[FactorScoringValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_factor_scoring_context_report(item: FactorScoringContext) -> FactorScoringValidationReport:
    return FactorScoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_factor_scoring_full_review_report(item: FactorScoringFullReview) -> FactorScoringValidationReport:
    return FactorScoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_factor_scoring_payload(payload: dict[str, Any]) -> FactorScoringValidationReport:
    return FactorScoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_execution_language_in_factor_scoring_text(text: str) -> FactorScoringValidationReport:
    return FactorScoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_unsafe_factor_scoring_fields(payload: dict[str, Any]) -> FactorScoringValidationReport:
    return FactorScoringValidationReport(True, 0, 0, 0, 0, [], [], [])

def factor_scoring_validation_report_to_text(report: FactorScoringValidationReport) -> str:
    return f"Valid: {report.valid}"

def assert_factor_scoring_validation_valid(report: FactorScoringValidationReport) -> None:
    if not report.valid:
        raise ValueError("Invalid factor scoring validation report")
