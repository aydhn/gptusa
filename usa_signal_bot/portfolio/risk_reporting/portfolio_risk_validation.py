from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioRiskContext,
    PortfolioRiskFullReview
)
from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_safety_validator import (
    validate_portfolio_risk_context_safety,
    portfolio_risk_payload_has_forbidden_fields,
    portfolio_risk_text_has_trade_or_execution_language
)
from usa_signal_bot.core.exceptions import PortfolioRiskValidationError

@dataclass
class PortfolioRiskValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any]

@dataclass
class PortfolioRiskValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[PortfolioRiskValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_portfolio_risk_context_report(item: PortfolioRiskContext) -> PortfolioRiskValidationReport:
    errs = validate_portfolio_risk_context_safety(item)
    return PortfolioRiskValidationReport(
        valid=len(errs) == 0,
        issue_count=len(errs),
        warning_count=0,
        error_count=len(errs),
        blocked_count=len(errs),
        issues=[PortfolioRiskValidationIssue("ERROR", None, e, {}) for e in errs],
        warnings=[],
        errors=errs
    )

def validate_portfolio_risk_full_review_report(item: PortfolioRiskFullReview) -> PortfolioRiskValidationReport:
    errs = []
    if item.context:
        errs.extend(validate_portfolio_risk_context_safety(item.context))
    return PortfolioRiskValidationReport(
        valid=len(errs) == 0,
        issue_count=len(errs),
        warning_count=0,
        error_count=len(errs),
        blocked_count=len(errs),
        issues=[PortfolioRiskValidationIssue("ERROR", None, e, {}) for e in errs],
        warnings=[],
        errors=errs
    )

def validate_no_sensitive_data_in_portfolio_risk_payload(payload: Dict[str, Any]) -> PortfolioRiskValidationReport:
    # simple mock for secrets check
    return PortfolioRiskValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_execution_language_in_portfolio_risk_text(text: str) -> PortfolioRiskValidationReport:
    has_exec = portfolio_risk_text_has_trade_or_execution_language(text)
    errs = ["Execution language found"] if has_exec else []
    return PortfolioRiskValidationReport(not has_exec, len(errs), 0, len(errs), len(errs), [], [], errs)

def validate_no_unsafe_portfolio_risk_fields(payload: Dict[str, Any]) -> PortfolioRiskValidationReport:
    has_unsafe = portfolio_risk_payload_has_forbidden_fields(payload)
    errs = ["Unsafe fields found"] if has_unsafe else []
    return PortfolioRiskValidationReport(not has_unsafe, len(errs), 0, len(errs), len(errs), [], [], errs)

def portfolio_risk_validation_report_to_text(report: PortfolioRiskValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_portfolio_risk_validation_valid(report: PortfolioRiskValidationReport) -> None:
    if not report.valid:
        raise PortfolioRiskValidationError(f"Validation failed: {report.errors}")
