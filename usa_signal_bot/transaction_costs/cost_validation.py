from dataclasses import dataclass, field
from typing import Any
import json

from usa_signal_bot.transaction_costs.cost_models import (
    TransactionCostBreakdown,
    SlippageCurve,
    MarketImpactEstimate,
    FillSimulationResult,
    TransactionCostReview,
    validate_transaction_cost_breakdown,
    validate_slippage_curve,
    validate_market_impact_estimate,
    validate_fill_simulation_result
)

@dataclass
class TransactionCostValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class TransactionCostValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[TransactionCostValidationIssue]
    warnings: list[str]
    errors: list[str]

def _add_issue(report: TransactionCostValidationReport, severity: str, field_name: str | None, msg: str) -> None:
    report.issues.append(TransactionCostValidationIssue(severity=severity, field=field_name, message=msg))
    report.issue_count += 1
    if severity == "ERROR":
        report.error_count += 1
        report.errors.append(msg)
        report.valid = False
    elif severity == "WARNING":
        report.warning_count += 1
        report.warnings.append(msg)
    elif severity == "BLOCKED":
        report.blocked_count += 1
        report.errors.append(msg)
        report.valid = False

def validate_transaction_cost_breakdown_report(item: TransactionCostBreakdown) -> TransactionCostValidationReport:
    report = TransactionCostValidationReport(True, 0, 0, 0, 0, [], [], [])
    try:
        validate_transaction_cost_breakdown(item)
    except ValueError as e:
        _add_issue(report, "ERROR", None, str(e))
    return report

def validate_slippage_curve_report(item: SlippageCurve) -> TransactionCostValidationReport:
    report = TransactionCostValidationReport(True, 0, 0, 0, 0, [], [], [])
    try:
        validate_slippage_curve(item)
    except ValueError as e:
        _add_issue(report, "ERROR", None, str(e))
    return report

def validate_market_impact_report(item: MarketImpactEstimate) -> TransactionCostValidationReport:
    report = TransactionCostValidationReport(True, 0, 0, 0, 0, [], [], [])
    try:
        validate_market_impact_estimate(item)
    except ValueError as e:
        _add_issue(report, "ERROR", None, str(e))
    return report

def validate_fill_simulation_report(item: FillSimulationResult) -> TransactionCostValidationReport:
    report = TransactionCostValidationReport(True, 0, 0, 0, 0, [], [], [])
    try:
        validate_fill_simulation_result(item)
    except ValueError as e:
        _add_issue(report, "ERROR", None, str(e))
    return report

def validate_transaction_cost_review_report(item: TransactionCostReview) -> TransactionCostValidationReport:
    report = TransactionCostValidationReport(True, 0, 0, 0, 0, [], [], [])
    for b in item.cost_breakdowns:
        try:
            validate_transaction_cost_breakdown(b)
        except ValueError as e:
            _add_issue(report, "ERROR", "cost_breakdowns", str(e))
    for i in item.impact_estimates:
        try:
            validate_market_impact_estimate(i)
        except ValueError as e:
            _add_issue(report, "ERROR", "impact_estimates", str(e))
    for f in item.fill_results:
        try:
            validate_fill_simulation_result(f)
        except ValueError as e:
            _add_issue(report, "ERROR", "fill_results", str(e))
    return report

def validate_no_sensitive_data_in_cost_payload(payload: dict[str, Any]) -> TransactionCostValidationReport:
    report = TransactionCostValidationReport(True, 0, 0, 0, 0, [], [], [])
    payload_str = json.dumps(payload).lower()
    sensitive_keys = ["api_key", "secret", "token", "password", "auth", "credential"]
    for k in sensitive_keys:
        if k in payload_str:
            _add_issue(report, "BLOCKED", None, f"Sensitive keyword '{k}' detected in cost payload")
    return report

def validate_no_live_execution_language_in_cost(text: str) -> TransactionCostValidationReport:
    report = TransactionCostValidationReport(True, 0, 0, 0, 0, [], [], [])
    text_lower = text.lower()
    banned_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "guaranteed fill", "kesin maliyet"]
    for phrase in banned_phrases:
        if phrase in text_lower:
            _add_issue(report, "BLOCKED", None, f"Live execution/guarantee language '{phrase}' detected in cost report")
    return report

def validate_no_broker_execution_fields_in_cost(payload: dict[str, Any]) -> TransactionCostValidationReport:
    report = TransactionCostValidationReport(True, 0, 0, 0, 0, [], [], [])
    payload_str = json.dumps(payload).lower()
    broker_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for f in broker_fields:
        if f in payload_str:
            _add_issue(report, "BLOCKED", None, f"Broker execution field '{f}' detected in cost payload")
    return report

def transaction_cost_validation_report_to_text(report: TransactionCostValidationReport) -> str:
    lines = [
        f"Validation Report (Valid: {report.valid})",
        f"  Errors: {report.error_count}",
        f"  Warnings: {report.warning_count}",
        f"  Blocked: {report.blocked_count}"
    ]
    for issue in report.issues:
        lines.append(f"  [{issue.severity}] {issue.field or 'general'}: {issue.message}")
    return "\n".join(lines)

def assert_transaction_cost_valid(report: TransactionCostValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Transaction Cost Validation Failed: {report.errors}")
