from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.risk.risk_models import RiskDecision, RiskRunResult, PositionSizingResult
from usa_signal_bot.risk.exposure_guard import ExposureSnapshot
from usa_signal_bot.core.enums import RiskDecisionStatus
from usa_signal_bot.core.exceptions import RiskValidationError

@dataclass
class RiskValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class RiskValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: list[RiskValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_risk_decision(decision: RiskDecision) -> RiskValidationReport:
    issues = []

    if decision.approved_quantity < 0:
        issues.append(RiskValidationIssue("error", "approved_quantity", "Negative approved quantity"))

    if decision.status == RiskDecisionStatus.REJECTED and decision.approved_quantity > 0:
        issues.append(RiskValidationIssue("error", "approved_quantity", "Rejected decision has >0 approved quantity"))

    if "broker_order" in decision.metadata or "live_order" in decision.metadata:
         issues.append(RiskValidationIssue("error", "metadata", "Broker/live order data found in risk decision!"))

    errors = [i.message for i in issues if i.severity == "error"]
    warnings = [i.message for i in issues if i.severity == "warning"]

    return RiskValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_risk_run_result(result: RiskRunResult) -> RiskValidationReport:
    issues = []

    calc_approved = sum(1 for d in result.decisions if d.status == RiskDecisionStatus.APPROVED)
    if calc_approved != result.approved_count:
        issues.append(RiskValidationIssue("error", "approved_count", "Mismatch in approved count"))

    if "broker_order" in result.__dict__ or "live_order" in result.__dict__:
        issues.append(RiskValidationIssue("error", "root", "Broker/live order data found in risk run result!"))

    errors = [i.message for i in issues if i.severity == "error"]
    warnings = [i.message for i in issues if i.severity == "warning"]

    return RiskValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_exposure_snapshot(snapshot: ExposureSnapshot) -> RiskValidationReport:
    issues = []

    if snapshot.portfolio_equity <= 0:
        issues.append(RiskValidationIssue("error", "portfolio_equity", "Negative or zero portfolio equity"))

    if snapshot.available_cash < 0:
        issues.append(RiskValidationIssue("error", "available_cash", "Negative available cash"))

    errors = [i.message for i in issues if i.severity == "error"]
    warnings = [i.message for i in issues if i.severity == "warning"]

    return RiskValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_position_sizing_result_for_decision(sizing: PositionSizingResult, decision: RiskDecision) -> RiskValidationReport:
    issues = []
    if sizing.approved_quantity != decision.approved_quantity and decision.status != RiskDecisionStatus.REJECTED:
        issues.append(RiskValidationIssue("warning", "approved_quantity", "Sizing result qty differs from decision qty"))

    errors = [i.message for i in issues if i.severity == "error"]
    warnings = [i.message for i in issues if i.severity == "warning"]

    return RiskValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_no_broker_execution_in_risk(result: RiskRunResult) -> RiskValidationReport:
    return validate_risk_run_result(result)

def risk_validation_report_to_text(report: RiskValidationReport) -> str:
    lines = [f"Valid: {report.valid}", f"Errors: {report.error_count}, Warnings: {report.warning_count}"]
    for i in report.issues:
        lines.append(f" - [{i.severity.upper()}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_risk_valid(report: RiskValidationReport) -> None:
    if not report.valid:
        raise RiskValidationError(f"Risk validation failed: {risk_validation_report_to_text(report)}")
