from dataclasses import dataclass, field
from typing import Any, Dict, List
import json
from usa_signal_bot.core.exceptions import AllocationValidationError
from usa_signal_bot.allocation.allocation_models import CapitalState, RiskBudget, PositionSizeResult, AllocationReview

@dataclass
class AllocationValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AllocationValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[AllocationValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[AllocationValidationIssue]) -> AllocationValidationReport:
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARNING"]
    return AllocationValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=0,
        issues=issues,
        warnings=[i.message for i in warnings],
        errors=[i.message for i in errors]
    )

def validate_capital_state_report(item: CapitalState) -> AllocationValidationReport:
    issues = []
    if item.total_equity_usd <= 0:
        issues.append(AllocationValidationIssue("ERROR", "total_equity_usd", "Total equity must be positive."))
    if item.available_cash_usd < 0:
        issues.append(AllocationValidationIssue("ERROR", "available_cash_usd", "Available cash cannot be negative."))
    return _create_report(issues)

def validate_risk_budget_report(item: RiskBudget) -> AllocationValidationReport:
    issues = []
    if not (0 <= item.portfolio_risk_budget_pct <= 100):
        issues.append(AllocationValidationIssue("ERROR", "portfolio_risk_budget_pct", "Must be between 0 and 100."))
    if not (0 <= item.per_trade_risk_budget_pct <= 100):
        issues.append(AllocationValidationIssue("ERROR", "per_trade_risk_budget_pct", "Must be between 0 and 100."))
    return _create_report(issues)

def validate_position_size_result_report(item: PositionSizeResult) -> AllocationValidationReport:
    issues = []
    if item.final_notional_usd is not None and item.final_notional_usd < 0:
        issues.append(AllocationValidationIssue("ERROR", "final_notional_usd", "Final notional cannot be negative."))
    if item.final_quantity is not None and item.final_quantity < 0:
        issues.append(AllocationValidationIssue("ERROR", "final_quantity", "Final quantity cannot be negative."))
    return _create_report(issues)

def validate_allocation_review_report(item: AllocationReview) -> AllocationValidationReport:
    issues = []
    if item.capital_state:
        sub = validate_capital_state_report(item.capital_state)
        issues.extend(sub.issues)
    if item.risk_budget:
        sub = validate_risk_budget_report(item.risk_budget)
        issues.extend(sub.issues)
    for res in item.sizing_results:
        sub = validate_position_size_result_report(res)
        issues.extend(sub.issues)
    return _create_report(issues)

def validate_no_sensitive_data_in_allocation_payload(payload: Dict[str, Any]) -> AllocationValidationReport:
    issues = []
    s_payload = json.dumps(payload).lower()
    for bad in ["api_key", "secret", "token", "password"]:
        if bad in s_payload:
            issues.append(AllocationValidationIssue("ERROR", "payload", f"Found potentially sensitive token/secret word: {bad}"))
    return _create_report(issues)

def validate_no_live_execution_language_in_allocation(text: str) -> AllocationValidationReport:
    issues = []
    tl = text.lower()
    bad_phrases = [
        "live approved", "sent to broker", "kesin al", "garanti",
        "kesin kâr", "kesin pozisyon", "şu kadar lot kesin alınmalı"
    ]
    for p in bad_phrases:
        if p in tl:
            issues.append(AllocationValidationIssue("ERROR", "language", f"Found live execution or advice language: '{p}'"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_allocation(payload: Dict[str, Any]) -> AllocationValidationReport:
    issues = []
    def _search(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
                    issues.append(AllocationValidationIssue("ERROR", k, f"Found prohibited broker field: {k}"))
                _search(v)
        elif isinstance(d, list):
            for i in d:
                _search(i)
    _search(payload)
    return _create_report(issues)

def allocation_validation_report_to_text(report: AllocationValidationReport) -> str:
    lines = [f"Allocation Validation Valid: {report.valid}"]
    lines.append(f"Errors: {report.error_count}, Warnings: {report.warning_count}")
    for i in report.issues:
        lines.append(f"[{i.severity}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_allocation_valid(report: AllocationValidationReport) -> None:
    if not report.valid:
        raise AllocationValidationError(f"Allocation validation failed:\n{allocation_validation_report_to_text(report)}")
