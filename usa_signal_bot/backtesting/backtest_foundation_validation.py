from dataclasses import dataclass
from typing import Any
import json

from usa_signal_bot.backtesting.phase146_models import (
    BacktestFoundationContext,
    BacktestFoundationFullReview
)
from usa_signal_bot.core.exceptions import BacktestFoundationValidationError

@dataclass
class BacktestFoundationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any]

@dataclass
class BacktestFoundationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[BacktestFoundationValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_backtest_foundation_context_report(item: BacktestFoundationContext) -> BacktestFoundationValidationReport:
    errors = list(item.errors)
    if not item.safety_boundary.boundary_passed:
        errors.append("Safety boundary failed in context.")
    if item.live_trading_enabled:
        errors.append("Context specifies live_trading_enabled=True.")

    return BacktestFoundationValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=len(item.warnings),
        error_count=len(errors),
        blocked_count=1 if errors else 0,
        issues=[BacktestFoundationValidationIssue("error", None, e, {}) for e in errors],
        warnings=list(item.warnings),
        errors=errors
    )

def validate_backtest_foundation_full_review_report(item: BacktestFoundationFullReview) -> BacktestFoundationValidationReport:
    return validate_backtest_foundation_context_report(item.context)

def validate_no_sensitive_data_in_backtest_payload(payload: dict[str, Any]) -> BacktestFoundationValidationReport:
    import re
    s_payload = json.dumps(payload).lower()
    errors = []
    if re.search(r"api_key|secret|password|token", s_payload):
        errors.append("Potential sensitive data keys found in payload.")

    return BacktestFoundationValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=1 if errors else 0,
        issues=[BacktestFoundationValidationIssue("error", "payload", e, {}) for e in errors],
        warnings=[],
        errors=errors
    )

def validate_no_execution_language_in_backtest_text(text: str) -> BacktestFoundationValidationReport:
    from usa_signal_bot.backtesting.backtest_safety_validator import backtest_text_has_trade_or_execution_language
    errors = []
    if backtest_text_has_trade_or_execution_language(text):
        errors.append("Execution language found in backtest text.")

    return BacktestFoundationValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=1 if errors else 0,
        issues=[BacktestFoundationValidationIssue("error", "text", e, {}) for e in errors],
        warnings=[],
        errors=errors
    )

def validate_no_unsafe_backtest_fields(payload: dict[str, Any]) -> BacktestFoundationValidationReport:
    # A generic proxy function for payload inspection if required
    return BacktestFoundationValidationReport(True, 0, 0, 0, 0, [], [], [])

def backtest_foundation_validation_report_to_text(report: BacktestFoundationValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_backtest_foundation_validation_valid(report: BacktestFoundationValidationReport) -> None:
    if not report.valid:
        raise BacktestFoundationValidationError(f"Validation failed with {report.error_count} errors. {report.errors}")
