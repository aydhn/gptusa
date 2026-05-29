from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    MarketBehaviorContext, MarketBehaviorFullReview, validate_market_behavior_full_review
)

@dataclass
class MarketBehaviorValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketBehaviorValidationReport:
    valid: bool = True
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: list[MarketBehaviorValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_market_behavior_context_report(item: MarketBehaviorContext) -> MarketBehaviorValidationReport:
    rep = MarketBehaviorValidationReport()
    errs = []
    # Simplified
    if item.activation_allowed: errs.append("activation_allowed is true")
    rep.valid = len(errs) == 0
    rep.errors = errs
    return rep

def validate_market_behavior_full_review_report(item: MarketBehaviorFullReview) -> MarketBehaviorValidationReport:
    rep = MarketBehaviorValidationReport()
    errs = validate_market_behavior_full_review(item)
    rep.valid = len(errs) == 0
    rep.errors = errs
    return rep

def validate_no_sensitive_data_in_market_behavior_payload(payload: dict[str, Any]) -> MarketBehaviorValidationReport:
    rep = MarketBehaviorValidationReport()
    from usa_signal_bot.regime_classification.behavior_reporting.diagnostics_artifact_loader import validate_diagnostics_artifact_payloads
    errs = validate_diagnostics_artifact_payloads({"p": [payload]})
    rep.valid = len(errs) == 0
    rep.errors = errs
    return rep

def validate_no_execution_language_in_market_behavior_text(text: str) -> MarketBehaviorValidationReport:
    rep = MarketBehaviorValidationReport()
    from usa_signal_bot.regime_classification.behavior_reporting.market_behavior_safety_validator import market_behavior_text_has_trade_or_execution_language
    if market_behavior_text_has_trade_or_execution_language(text):
        rep.valid = False
        rep.errors.append("Unsafe execution language found.")
    return rep

def validate_no_unsafe_market_behavior_fields(payload: dict[str, Any]) -> MarketBehaviorValidationReport:
    return validate_no_sensitive_data_in_market_behavior_payload(payload)

def market_behavior_validation_report_to_text(report: MarketBehaviorValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {len(report.errors)}"

def assert_market_behavior_validation_valid(report: MarketBehaviorValidationReport) -> None:
    if not report.valid:
        raise Exception(f"Validation failed: {report.errors}")
