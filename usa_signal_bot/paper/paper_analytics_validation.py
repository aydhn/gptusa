from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

from usa_signal_bot.paper.paper_analytics_models import PaperPerformanceReport
from usa_signal_bot.paper.paper_risk_report import PaperRiskReport
from usa_signal_bot.paper.paper_drawdown_monitor import PaperDrawdownReport
from usa_signal_bot.paper.paper_rolling_metrics import PaperRollingMetricsReport
from usa_signal_bot.core.exceptions import PaperAnalyticsValidationError

@dataclass
class PaperAnalyticsValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperAnalyticsValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: List[PaperAnalyticsValidationIssue]
    warnings: List[str]
    errors: List[str]

def _build_validation_report(issues: List[PaperAnalyticsValidationIssue]) -> PaperAnalyticsValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    return PaperAnalyticsValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_paper_performance_report_report(report: PaperPerformanceReport) -> PaperAnalyticsValidationReport:
    issues = []

    if report.equity_metrics.max_drawdown_pct is not None and report.equity_metrics.max_drawdown_pct < 0:
        issues.append(PaperAnalyticsValidationIssue("ERROR", "max_drawdown_pct", "Drawdown percentage cannot be negative."))
    if report.trade_metrics.win_rate is not None and not (0.0 <= report.trade_metrics.win_rate <= 1.0):
        issues.append(PaperAnalyticsValidationIssue("ERROR", "win_rate", "Win rate must be between 0 and 1."))
    if report.trade_metrics.profit_factor is not None and report.trade_metrics.profit_factor < 0:
        issues.append(PaperAnalyticsValidationIssue("ERROR", "profit_factor", "Profit factor cannot be negative."))

    return _build_validation_report(issues)

def validate_paper_risk_report_report(report: PaperRiskReport) -> PaperAnalyticsValidationReport:
    issues = []
    if report.risk_level.value not in ["LOW", "MODERATE", "HIGH", "CRITICAL", "UNKNOWN"]:
        issues.append(PaperAnalyticsValidationIssue("ERROR", "risk_level", f"Invalid risk level: {report.risk_level.value}"))
    return _build_validation_report(issues)

def validate_paper_drawdown_report_report(report: PaperDrawdownReport) -> PaperAnalyticsValidationReport:
    issues = []
    if report.max_drawdown_pct is not None and report.max_drawdown_pct < 0:
        issues.append(PaperAnalyticsValidationIssue("ERROR", "max_drawdown_pct", "Max drawdown percentage cannot be negative."))
    return _build_validation_report(issues)

def validate_paper_rolling_metrics_report_report(report: PaperRollingMetricsReport) -> PaperAnalyticsValidationReport:
    issues = []
    if report.window_size <= 0:
        issues.append(PaperAnalyticsValidationIssue("ERROR", "window_size", "Window size must be positive."))
    return _build_validation_report(issues)

def validate_no_broker_execution_in_paper_analytics(payload: Dict[str, Any]) -> PaperAnalyticsValidationReport:
    issues = []
    payload_str = json.dumps(payload).lower()

    forbidden_terms = ["live_order", "demo_broker", "broker_id", "alpaca_order_id", "ibkr_id"]
    for term in forbidden_terms:
        if term in payload_str:
            issues.append(PaperAnalyticsValidationIssue("ERROR", None, f"Forbidden term found in analytics payload: {term}"))

    return _build_validation_report(issues)

def validate_no_investment_advice_language_in_paper_analytics(text: str) -> PaperAnalyticsValidationReport:
    issues = []
    text_lower = text.lower()

    forbidden_phrases = ["buy now", "sell now", "kesin al", "kesin sat", "garanti", "investment advice"]
    for phrase in forbidden_phrases:
        # Check if the phrase is used incorrectly (i.e. not in a disclaimer)
        if phrase in text_lower and phrase != "investment advice" and "not investment advice" not in text_lower:
             issues.append(PaperAnalyticsValidationIssue("ERROR", None, f"Forbidden investment advice language found: {phrase}"))
        elif phrase == "investment advice" and "not investment advice" not in text_lower:
             issues.append(PaperAnalyticsValidationIssue("ERROR", None, f"Must explicitly state 'not investment advice'."))

    return _build_validation_report(issues)

def paper_analytics_validation_report_to_text(report: PaperAnalyticsValidationReport) -> str:
    lines = [
        f"Validation Valid: {report.valid}",
        f"Issues: {report.issue_count} (Warnings: {report.warning_count}, Errors: {report.error_count})"
    ]
    for issue in report.issues:
        lines.append(f"- [{issue.severity}] {issue.field or 'General'}: {issue.message}")
    return "\n".join(lines)

def assert_paper_analytics_valid(report: PaperAnalyticsValidationReport) -> None:
    if not report.valid:
        raise PaperAnalyticsValidationError(f"Analytics validation failed with {report.error_count} errors:\n{paper_analytics_validation_report_to_text(report)}")
