"""Validation for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.exceptions import BacktestValidationError

@dataclass
class BacktestValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: list[BacktestValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_backtest_run_config(config: Any) -> BacktestValidationReport:
    issues = []

    if config.starting_cash <= 0:
        issues.append(BacktestValidationIssue("ERROR", "starting_cash", "Must be > 0"))
    if config.fee_rate < 0:
        issues.append(BacktestValidationIssue("ERROR", "fee_rate", "Cannot be negative"))
    if config.slippage_bps < 0:
        issues.append(BacktestValidationIssue("ERROR", "slippage_bps", "Cannot be negative"))
    if config.hold_bars <= 0:
        issues.append(BacktestValidationIssue("ERROR", "hold_bars", "Must be positive"))

    if config.signal_to_order.allow_short:
        issues.append(BacktestValidationIssue("WARNING", "allow_short", "Shorting is not fully supported in Phase 25. Usage is at your own risk."))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return BacktestValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_backtest_run_request(request: Any) -> BacktestValidationReport:
    issues = []

    if not request.symbols:
        issues.append(BacktestValidationIssue("ERROR", "symbols", "Symbols list cannot be empty"))
    if not request.timeframe:
        issues.append(BacktestValidationIssue("ERROR", "timeframe", "Timeframe cannot be empty"))

    if not request.signal_file and not request.selected_candidates_file:
        issues.append(BacktestValidationIssue("ERROR", "signal_file", "Must provide either signal_file or selected_candidates_file"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return BacktestValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_backtest_result(result: Any) -> BacktestValidationReport:
    issues = []
    if len(result.snapshots) == 0 and result.portfolio.cash == result.portfolio.starting_cash and not result.fills:
        issues.append(BacktestValidationIssue("WARNING", "snapshots", "No snapshots generated, empty backtest."))

    if result.metrics.status.value == "EMPTY":
        issues.append(BacktestValidationIssue("WARNING", "metrics", "Backtest metric status is EMPTY. No trades taken."))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return BacktestValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_no_broker_execution(result: Any) -> BacktestValidationReport:
    issues = []

    for order in result.order_intents:
        if "broker_order_id" in order.metadata:
            issues.append(BacktestValidationIssue("ERROR", "order_intents", "Order contains broker_order_id. This engine MUST NOT execute real orders."))

    for fill in result.fills:
        if "broker_execution_id" in fill.metadata:
            issues.append(BacktestValidationIssue("ERROR", "fills", "Fill contains broker_execution_id. This engine MUST NOT interact with real brokers."))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return BacktestValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def backtest_validation_report_to_text(report: BacktestValidationReport) -> str:
    lines = [
        "=== Backtest Validation Report ===",
        f"Valid:           {report.valid}",
        f"Total Issues:    {report.issue_count}",
        f"Warnings:        {report.warning_count}",
        f"Errors:          {report.error_count}"
    ]
    if report.issues:
        lines.append("\nIssues Details:")
        for issue in report.issues:
            lines.append(f"  [{issue.severity}] {issue.field}: {issue.message}")
    return "\n".join(lines)

def assert_backtest_valid(report: BacktestValidationReport) -> None:
    if not report.valid:
        raise BacktestValidationError(f"Backtest validation failed: {report.errors}")
