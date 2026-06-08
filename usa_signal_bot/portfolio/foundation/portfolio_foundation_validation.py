from typing import Any
from dataclasses import dataclass, field

from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioFoundationContext, PortfolioFoundationFullReview
)
from usa_signal_bot.portfolio.foundation.portfolio_foundation_safety_validator import (
    portfolio_payload_has_forbidden_fields, portfolio_foundation_text_has_trade_or_execution_language
)

@dataclass
class PortfolioFoundationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioFoundationValidationReport:
    valid: bool = False
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: list[PortfolioFoundationValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_no_sensitive_data_in_portfolio_foundation_payload(payload: dict[str, Any]) -> PortfolioFoundationValidationReport:
    report = PortfolioFoundationValidationReport(valid=True)
    if portfolio_payload_has_forbidden_fields(payload):
        report.valid = False
        report.error_count += 1
        report.errors.append("Payload contains forbidden portfolio/execution fields")
    return report

def validate_no_unsafe_portfolio_foundation_fields(payload: dict[str, Any]) -> PortfolioFoundationValidationReport:
    return validate_no_sensitive_data_in_portfolio_foundation_payload(payload)

def validate_no_execution_language_in_portfolio_foundation_text(text: str) -> PortfolioFoundationValidationReport:
    report = PortfolioFoundationValidationReport(valid=True)
    if portfolio_foundation_text_has_trade_or_execution_language(text):
        report.valid = False
        report.error_count += 1
        report.errors.append("Text contains execution or trade language")
    return report

def validate_portfolio_foundation_context_report(item: PortfolioFoundationContext) -> PortfolioFoundationValidationReport:
    report = PortfolioFoundationValidationReport(valid=True)
    if not item.safety_boundary.boundary_passed:
        report.valid = False
        report.error_count += 1
        report.errors.append("Safety boundary failed")
    if not item.phase154_readiness_gate.ready_for_phase154:
        report.valid = False
        report.error_count += 1
        report.errors.append("Phase 154 readiness gate not passed")
    return report

def validate_portfolio_foundation_full_review_report(item: PortfolioFoundationFullReview) -> PortfolioFoundationValidationReport:
    return validate_portfolio_foundation_context_report(item.context)

def portfolio_foundation_validation_report_to_text(report: PortfolioFoundationValidationReport) -> str:
    return f"ValidationReport: valid={report.valid}, errors={report.error_count}"

def assert_portfolio_foundation_validation_valid(report: PortfolioFoundationValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Portfolio foundation validation failed: {report.errors}")
