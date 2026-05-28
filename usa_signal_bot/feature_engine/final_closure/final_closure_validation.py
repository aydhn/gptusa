import json
from dataclasses import dataclass, field
from typing import Any, Dict, List
from usa_signal_bot.feature_engine.final_closure.phase125_models import FinalClosureContext, FinalClosureFullReview
from usa_signal_bot.feature_engine.final_closure.final_closure_safety_validator import (
    validate_final_closure_context_safety,
    final_closure_text_has_trade_or_execution_language
)
from usa_signal_bot.core.exceptions import FinalClosureValidationError

@dataclass
class FinalClosureValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalClosureValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[FinalClosureValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[FinalClosureValidationIssue], errs: List[str]) -> FinalClosureValidationReport:
    return FinalClosureValidationReport(
        valid=len(errs) == 0,
        issue_count=len(issues),
        warning_count=sum(1 for i in issues if i.severity == "warning"),
        error_count=sum(1 for i in issues if i.severity == "error"),
        blocked_count=sum(1 for i in issues if i.severity == "blocked"),
        issues=issues,
        warnings=[],
        errors=errs
    )

def validate_final_closure_context_report(item: FinalClosureContext) -> FinalClosureValidationReport:
    errs = validate_final_closure_context_safety(item)
    issues = [FinalClosureValidationIssue(severity="error", field=None, message=e) for e in errs]
    return _create_report(issues, errs)

def validate_final_closure_full_review_report(item: FinalClosureFullReview) -> FinalClosureValidationReport:
    return validate_final_closure_context_report(item.context)

def validate_no_sensitive_data_in_final_closure_payload(payload: Dict[str, Any]) -> FinalClosureValidationReport:
    payload_str = json.dumps(payload).lower()
    errs = []
    sensitive_keys = ["api_key", "token", "secret", "password", "broker_order_id", "live_order_id", "sent_to_broker"]
    for sk in sensitive_keys:
        if sk in payload_str:
            errs.append(f"Found sensitive key: {sk}")
    issues = [FinalClosureValidationIssue(severity="error", field=None, message=e) for e in errs]
    return _create_report(issues, errs)

def validate_no_execution_language_in_final_closure_text(text: str) -> FinalClosureValidationReport:
    errs = []
    if final_closure_text_has_trade_or_execution_language(text):
        errs.append("Text contains execution or trading advice language")
    issues = [FinalClosureValidationIssue(severity="error", field=None, message=e) for e in errs]
    return _create_report(issues, errs)

def validate_no_unsafe_final_closure_fields(payload: Dict[str, Any]) -> FinalClosureValidationReport:
    errs = []
    unsafe_fields = [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled",
        "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled",
        "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]
    for field in unsafe_fields:
        if payload.get(field) is True:
            errs.append(f"{field} must be false")
    issues = [FinalClosureValidationIssue(severity="error", field=field, message=e) for e in errs]
    return _create_report(issues, errs)

def final_closure_validation_report_to_text(report: FinalClosureValidationReport) -> str:
    if report.valid:
        return "ValidationReport: Valid"
    return f"ValidationReport: Invalid ({report.error_count} errors)"

def assert_final_closure_validation_valid(report: FinalClosureValidationReport) -> None:
    if not report.valid:
        raise FinalClosureValidationError(f"Final closure validation failed: {report.errors}")
