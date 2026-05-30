from typing import Any, Dict, List
from dataclasses import dataclass, field
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeResearchFreezeContext,
    RegimeResearchFreezeFullReview
)
from usa_signal_bot.core.exceptions import ResearchFreezeValidationError

@dataclass
class ResearchFreezeValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchFreezeValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ResearchFreezeValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def validate_regime_research_freeze_context_report(item: RegimeResearchFreezeContext) -> ResearchFreezeValidationReport:
    errors = []
    if not item.context_id:
        errors.append("Missing context_id")
    return ResearchFreezeValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        errors=errors
    )

def validate_regime_research_freeze_full_review_report(item: RegimeResearchFreezeFullReview) -> ResearchFreezeValidationReport:
    errors = []
    if not item.review_id:
        errors.append("Missing review_id")
    return ResearchFreezeValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        errors=errors
    )

def validate_no_sensitive_data_in_research_freeze_payload(payload: Dict[str, Any]) -> ResearchFreezeValidationReport:
    errors = []
    import json
    text = json.dumps(payload).lower()
    for s in ["api_key", "password", "secret", "token"]:
        if s in text:
            errors.append(f"Sensitive keyword detected: {s}")
    return ResearchFreezeValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        errors=errors
    )

def validate_no_execution_language_in_research_freeze_text(text: str) -> ResearchFreezeValidationReport:
    from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_safety_validator import research_freeze_text_has_trade_or_execution_language
    errors = []
    if research_freeze_text_has_trade_or_execution_language(text):
        errors.append("Execution language detected in text")
    return ResearchFreezeValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=0,
        errors=errors
    )

def validate_no_unsafe_research_freeze_fields(payload: Dict[str, Any]) -> ResearchFreezeValidationReport:
    return validate_no_sensitive_data_in_research_freeze_payload(payload)

def research_freeze_validation_report_to_text(report: ResearchFreezeValidationReport) -> str:
    if report.valid:
        return "Validation Report: Valid."
    return f"Validation Report: Failed with {report.error_count} errors:\n" + "\n".join(f"- {e}" for e in report.errors)

def assert_research_freeze_validation_valid(report: ResearchFreezeValidationReport) -> None:
    if not report.valid:
        raise ResearchFreezeValidationError(f"Validation failed: {report.errors}")
