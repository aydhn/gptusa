from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.backtesting.analytics.phase148_models import (
    BacktestAnalyticsContext,
    BacktestAnalyticsFullReview
)
from usa_signal_bot.core.exceptions import BacktestAnalyticsValidationError

@dataclass
class BacktestAnalyticsValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestAnalyticsValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[BacktestAnalyticsValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_backtest_analytics_context_report(item: BacktestAnalyticsContext) -> BacktestAnalyticsValidationReport:
    raise NotImplementedError()

def validate_backtest_analytics_full_review_report(item: BacktestAnalyticsFullReview) -> BacktestAnalyticsValidationReport:
    raise NotImplementedError()

def validate_no_sensitive_data_in_backtest_analytics_payload(payload: dict[str, Any]) -> BacktestAnalyticsValidationReport:
    raise NotImplementedError()

def validate_no_execution_language_in_backtest_analytics_text(text: str) -> BacktestAnalyticsValidationReport:
    raise NotImplementedError()

def validate_no_unsafe_backtest_analytics_fields(payload: dict[str, Any]) -> BacktestAnalyticsValidationReport:
    raise NotImplementedError()

def backtest_analytics_validation_report_to_text(report: BacktestAnalyticsValidationReport) -> str:
    raise NotImplementedError()

def assert_backtest_analytics_validation_valid(report: BacktestAnalyticsValidationReport) -> None:
    raise NotImplementedError()
