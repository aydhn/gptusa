from dataclasses import dataclass, field
from typing import Any, Dict, List
import json
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, DriftMeasurement,
    RebalanceAction, RebalancePlan, RebalanceReview
)

@dataclass
class RebalanceValidationIssue:
    severity: str
    message: str
    field_name: str | None = None
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RebalanceValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[RebalanceValidationIssue]
    warnings: List[str]
    errors: List[str]

def _build_empty_report() -> RebalanceValidationReport:
    return RebalanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def _add_error(report: RebalanceValidationReport, message: str, fld: str | None = None):
    report.valid = False
    report.error_count += 1
    report.issue_count += 1
    report.errors.append(message)
    report.issues.append(RebalanceValidationIssue("ERROR", message, fld))

def validate_current_portfolio_state_report(item: CurrentPortfolioState) -> RebalanceValidationReport:
    r = _build_empty_report()
    if item.total_equity_usd is not None and item.total_equity_usd < 0:
        _add_error(r, "total_equity_usd cannot be negative", "total_equity_usd")
    for pos in item.positions:
        if pos.quantity < 0:
            _add_error(r, f"Position {pos.symbol} has negative quantity", "quantity")
        if pos.market_value_usd < 0:
            _add_error(r, f"Position {pos.symbol} has negative market_value_usd", "market_value_usd")
    return r

def validate_target_portfolio_state_report(item: TargetPortfolioState) -> RebalanceValidationReport:
    r = _build_empty_report()
    if item.total_equity_usd is not None and item.total_equity_usd < 0:
        _add_error(r, "total_equity_usd cannot be negative", "total_equity_usd")
    for pos in item.target_positions:
        if pos.quantity < 0:
            _add_error(r, f"Target {pos.symbol} has negative quantity", "quantity")
        if pos.market_value_usd < 0:
            _add_error(r, f"Target {pos.symbol} has negative market_value_usd", "market_value_usd")
    return r

def validate_drift_measurements_report(items: List[DriftMeasurement]) -> RebalanceValidationReport:
    r = _build_empty_report()
    for item in items:
        if item.absolute_drift is not None and item.absolute_drift < 0:
            _add_error(r, f"Drift {item.name} has negative absolute_drift", "absolute_drift")
    return r

def validate_rebalance_actions_report(items: List[RebalanceAction]) -> RebalanceValidationReport:
    r = _build_empty_report()
    for item in items:
        if item.estimated_cost_usd is not None and item.estimated_cost_usd < 0:
            _add_error(r, f"Action {item.symbol} has negative estimated_cost_usd", "estimated_cost_usd")
        if item.estimated_turnover_usd is not None and item.estimated_turnover_usd < 0:
            _add_error(r, f"Action {item.symbol} has negative estimated_turnover_usd", "estimated_turnover_usd")
        if item.current_notional_usd is not None and item.delta_notional_usd is not None:
            if item.current_notional_usd + item.delta_notional_usd < -0.01:
                 _add_error(r, f"Action {item.symbol} creates negative position", "delta_notional_usd")
    return r

def validate_rebalance_plan_report(item: RebalancePlan) -> RebalanceValidationReport:
    r = _build_empty_report()

    if item.current_state:
        cs = validate_current_portfolio_state_report(item.current_state)
        r.valid = r.valid and cs.valid
        r.errors.extend(cs.errors)
        r.issues.extend(cs.issues)

    if item.target_state:
        ts = validate_target_portfolio_state_report(item.target_state)
        r.valid = r.valid and ts.valid
        r.errors.extend(ts.errors)
        r.issues.extend(ts.issues)

    act = validate_rebalance_actions_report(item.actions)
    r.valid = r.valid and act.valid
    r.errors.extend(act.errors)
    r.issues.extend(act.issues)

    return r

def validate_rebalance_review_report(item: RebalanceReview) -> RebalanceValidationReport:
    r = _build_empty_report()
    if item.plan:
        pr = validate_rebalance_plan_report(item.plan)
        r.valid = r.valid and pr.valid
        r.errors.extend(pr.errors)
        r.issues.extend(pr.issues)
    return r

def validate_no_sensitive_data_in_rebalance_payload(payload: Dict[str, Any]) -> RebalanceValidationReport:
    r = _build_empty_report()
    txt = json.dumps(payload).lower()
    for word in ["secret", "token", "api_key", "password", "alpaca_key", "alpaca_secret"]:
        if word in txt:
            _add_error(r, f"Sensitive word found: {word}", "payload")
    return r

def validate_no_live_execution_language_in_rebalance(text: str) -> RebalanceValidationReport:
    r = _build_empty_report()
    txt = text.lower()
    forbidden = ["live approved", "sent to broker", "kesin al", "garanti", "pozisyonu kesin artır", "kesin azalt", "kesin portföy"]
    for phrase in forbidden:
        if phrase in txt:
            _add_error(r, f"Forbidden language found: '{phrase}'", "text")
    return r

def validate_no_broker_execution_fields_in_rebalance(payload: Dict[str, Any]) -> RebalanceValidationReport:
    r = _build_empty_report()
    txt = json.dumps(payload).lower()
    for field in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if field in txt:
             _add_error(r, f"Broker field found: {field}", "payload")
    return r

def rebalance_validation_report_to_text(report: RebalanceValidationReport) -> str:
    if report.valid:
        return "Validation PASS"
    lines = ["Validation FAIL"]
    for e in report.errors:
        lines.append(f" - {e}")
    return "\n".join(lines)

def assert_rebalance_valid(report: RebalanceValidationReport) -> None:
    from usa_signal_bot.core.exceptions import RebalanceValidationError
    if not report.valid:
        raise RebalanceValidationError(f"Validation failed with {len(report.errors)} errors: {report.errors[0]}")
