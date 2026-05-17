"""Validation constraints and safety checks for attribution data."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import AttributionValidationError
from usa_signal_bot.attribution.attribution_models import (
    AttributionTradeEvent, AttributionContribution, RiskAttributionContribution,
    SignalContribution, AttributionScorecard, AttributionReview
)

@dataclass
class AttributionValidationIssue:
    severity: str
    message: str
    field_name: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AttributionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[AttributionValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[AttributionValidationIssue]) -> AttributionValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = [i.message for i in issues if i.severity == "BLOCKED"]

    return AttributionValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_attribution_events_report(items: List[AttributionTradeEvent]) -> AttributionValidationReport:
    issues = []
    for i, item in enumerate(items):
        if not item.symbol:
            issues.append(AttributionValidationIssue("ERROR", "Missing symbol", "symbol"))
        if item.quantity is not None and item.quantity < 0:
            issues.append(AttributionValidationIssue("ERROR", "Negative quantity", "quantity"))
        if item.notional_usd is not None and item.notional_usd < 0:
            issues.append(AttributionValidationIssue("ERROR", "Negative notional", "notional_usd"))
        if item.total_cost_usd is not None and item.total_cost_usd < 0:
            issues.append(AttributionValidationIssue("ERROR", "Negative cost", "total_cost_usd"))
    return _create_report(issues)

def validate_performance_contributions_report(items: List[AttributionContribution]) -> AttributionValidationReport:
    issues = []
    for item in items:
        if item.trade_count < 0:
            issues.append(AttributionValidationIssue("ERROR", "Negative trade count", "trade_count"))
        if item.win_rate is not None and (item.win_rate < 0 or item.win_rate > 100):
            issues.append(AttributionValidationIssue("ERROR", "Invalid win rate", "win_rate"))
    return _create_report(issues)

def validate_risk_contributions_report(items: List[RiskAttributionContribution]) -> AttributionValidationReport:
    return _create_report([])

def validate_signal_contributions_report(items: List[SignalContribution]) -> AttributionValidationReport:
    issues = []
    for item in items:
        if item.trade_count < 0:
            issues.append(AttributionValidationIssue("ERROR", "Negative trade count", "trade_count"))
        if item.win_rate is not None and (item.win_rate < 0 or item.win_rate > 100):
            issues.append(AttributionValidationIssue("ERROR", "Invalid win rate", "win_rate"))
    return _create_report(issues)

def validate_attribution_scorecard_report(item: AttributionScorecard) -> AttributionValidationReport:
    return _create_report([])

def validate_attribution_review_report(item: AttributionReview) -> AttributionValidationReport:
    reports = [
        validate_attribution_events_report(item.events),
        validate_performance_contributions_report(item.performance_contributions),
        validate_risk_contributions_report(item.risk_contributions),
        validate_signal_contributions_report(item.signal_contributions),
        validate_attribution_scorecard_report(item.scorecard) if item.scorecard else _create_report([])
    ]

    issues = []
    for r in reports:
        issues.extend(r.issues)
    return _create_report(issues)

def validate_no_broker_execution_fields_in_attribution(payload: Dict[str, Any]) -> AttributionValidationReport:
    import json
    text = json.dumps(payload).lower()
    broker_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    issues = []
    for field in broker_fields:
        if field in text:
            issues.append(AttributionValidationIssue("BLOCKED", f"Broker field found: {field}"))
    return _create_report(issues)

def validate_no_live_execution_language_in_attribution(text: str) -> AttributionValidationReport:
    text_lower = text.lower()
    banned_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "bu sinyal kesin çalışır", "kesin kâr", "kesin strateji"]
    issues = []
    for phrase in banned_phrases:
        if phrase in text_lower:
            issues.append(AttributionValidationIssue("BLOCKED", f"Banned certainty/live language found: '{phrase}'"))
    return _create_report(issues)

def validate_no_sensitive_data_in_attribution_payload(payload: Dict[str, Any]) -> AttributionValidationReport:
    import json
    text = json.dumps(payload).lower()
    issues = []
    if "api_key" in text or "secret" in text or "token" in text:
        issues.append(AttributionValidationIssue("ERROR", "Potential secret leak in payload"))
    return _create_report(issues)

def attribution_validation_report_to_text(report: AttributionValidationReport) -> str:
    lines = [f"Validation Report: {'VALID' if report.valid else 'INVALID'}"]
    for i in report.issues:
        lines.append(f"[{i.severity}] {i.message}")
    return "\n".join(lines)

def assert_attribution_valid(report: AttributionValidationReport) -> None:
    if not report.valid:
        raise AttributionValidationError(f"Attribution validation failed with {report.error_count} errors and {report.blocked_count} blocked issues.")
