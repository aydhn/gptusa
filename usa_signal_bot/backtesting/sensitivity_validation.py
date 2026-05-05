from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.exceptions import SensitivityValidationError
from usa_signal_bot.backtesting.backtest_engine import BacktestRunRequest
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterGridSpec, ParameterSensitivityConfig, SensitivityCellResult,
    ParameterSensitivityRunResult, SensitivityCellStatus
)

@dataclass
class SensitivityValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class SensitivityValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: list[SensitivityValidationIssue]
    warnings: list[str]
    errors: list[str]

def _create_report(issues: list[SensitivityValidationIssue]) -> SensitivityValidationReport:
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARNING"]

    return SensitivityValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=[w.message for w in warnings],
        errors=[e.message for e in errors]
    )

def validate_sensitivity_run_request(base_request: BacktestRunRequest, grid_spec: ParameterGridSpec, config: ParameterSensitivityConfig) -> SensitivityValidationReport:
    issues = []

    if not base_request.symbols:
        issues.append(SensitivityValidationIssue("ERROR", "symbols", "Base request must have symbols"))

    if grid_spec.max_cells > config.max_cells:
        issues.append(SensitivityValidationIssue("WARNING", "max_cells", f"Grid max_cells ({grid_spec.max_cells}) exceeds config max_cells ({config.max_cells})"))

    if not base_request.signal_file and not base_request.selected_candidates_file:
        issues.append(SensitivityValidationIssue("WARNING", "signal_file", "No signal file or candidates file provided in base request. Ensure strategy produces signals internally or this run may generate no trades."))

    return _create_report(issues)

def validate_grid_cell_results(results: list[SensitivityCellResult], min_completed_cells: int) -> SensitivityValidationReport:
    issues = []
    completed_cells = sum(1 for r in results if r.status == SensitivityCellStatus.COMPLETED)

    if completed_cells < min_completed_cells:
        issues.append(SensitivityValidationIssue("ERROR", "completed_cells", f"Only {completed_cells} cells completed, below minimum of {min_completed_cells}"))

    return _create_report(issues)

def validate_no_optimizer_behavior(result: ParameterSensitivityRunResult) -> SensitivityValidationReport:
    issues = []

    if hasattr(result, 'best_params') or hasattr(result, 'recommended_params'):
        issues.append(SensitivityValidationIssue("ERROR", "optimizer_behavior", "Result object contains 'best_params' or 'recommended_params'. Optimizer behavior is strictly forbidden in this phase."))

    # Check that aggregate_metrics doesn't have best param keys hidden in it
    for key in result.aggregate_metrics.keys():
        if "best" in key.lower() or "optimal" in key.lower() or "recommended" in key.lower():
            issues.append(SensitivityValidationIssue("ERROR", "optimizer_behavior", f"Metric key '{key}' implies optimization, which is forbidden."))

    return _create_report(issues)

def validate_sensitivity_run_result(result: ParameterSensitivityRunResult) -> SensitivityValidationReport:
    issues = []

    if not result.cells:
        issues.append(SensitivityValidationIssue("ERROR", "cells", "No cells in run result"))

    if len(result.cells) != len(result.cell_results):
        issues.append(SensitivityValidationIssue("ERROR", "cell_results", "Cell results count does not match cells count"))

    no_opt_report = validate_no_optimizer_behavior(result)
    issues.extend(no_opt_report.issues)

    return _create_report(issues)

def sensitivity_validation_report_to_text(report: SensitivityValidationReport) -> str:
    lines = [
        f"Validation Report (Valid: {report.valid})",
        f"Errors: {report.error_count}, Warnings: {report.warning_count}"
    ]
    for e in report.errors:
        lines.append(f"[ERROR] {e}")
    for w in report.warnings:
        lines.append(f"[WARNING] {w}")
    return "\n".join(lines)

def assert_sensitivity_valid(report: SensitivityValidationReport) -> None:
    if not report.valid:
        error_msgs = "\n".join(report.errors)
        raise SensitivityValidationError(f"Sensitivity validation failed:\n{error_msgs}")
