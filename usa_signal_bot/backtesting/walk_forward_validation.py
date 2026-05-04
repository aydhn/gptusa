from dataclasses import dataclass, field as dataclass_field
from typing import Any
from usa_signal_bot.core.exceptions import WalkForwardValidationError
from usa_signal_bot.backtesting.walk_forward_models import WalkForwardRunRequest, WalkForwardWindow, WalkForwardRunResult

@dataclass
class WalkForwardValidationIssue:
    severity: str
    message: str
    field: str | None = None
    details: dict[str, Any] = dataclass_field(default_factory=dict)

@dataclass
class WalkForwardValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: list[WalkForwardValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_walk_forward_run_request(request: WalkForwardRunRequest) -> WalkForwardValidationReport:
    issues = []

    if not request.symbols:
        issues.append(WalkForwardValidationIssue(severity="ERROR", field="symbols", message="Symbols list cannot be empty"))

    if not request.timeframe:
        issues.append(WalkForwardValidationIssue(severity="ERROR", field="timeframe", message="Timeframe cannot be empty"))

    if not request.signal_file and not request.selected_candidates_file:
        issues.append(WalkForwardValidationIssue(severity="ERROR", field="files", message="Either signal_file or selected_candidates_file must be provided"))

    if request.start_date and request.end_date:
        if request.start_date >= request.end_date:
            issues.append(WalkForwardValidationIssue(severity="ERROR", field="dates", message=f"start_date ({request.start_date}) must be before end_date ({request.end_date})"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return WalkForwardValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_walk_forward_windows(windows: list[WalkForwardWindow]) -> WalkForwardValidationReport:
    issues = []

    if not windows:
        issues.append(WalkForwardValidationIssue(severity="ERROR", message="Windows list is empty"))
    else:
        for i, w in enumerate(windows):
            try:
                from usa_signal_bot.backtesting.walk_forward_models import validate_walk_forward_window
                validate_walk_forward_window(w)
            except Exception as e:
                issues.append(WalkForwardValidationIssue(severity="ERROR", field=f"windows[{i}]", message=str(e)))

        # Check for overlapping test windows (might be warning or valid depending on mode, we just warn)
        for i in range(len(windows) - 1):
            if windows[i].test_end > windows[i+1].test_start:
                issues.append(WalkForwardValidationIssue(
                    severity="WARNING",
                    field="test_windows",
                    message=f"Test window overlap between {windows[i].window_id} and {windows[i+1].window_id}"
                ))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return WalkForwardValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_no_walk_forward_optimization(result: WalkForwardRunResult) -> WalkForwardValidationReport:
    issues = []
    # In Phase 28, there is no optimizer.
    # We assert that the run does not contain parameter search data.
    if "optimization" in result.aggregate_metrics or "optimized_params" in result.aggregate_metrics:
        issues.append(WalkForwardValidationIssue(severity="ERROR", message="Optimization is strictly forbidden in this phase"))

    # Check for live execution
    if any("live" in str(k).lower() for k in result.output_paths.keys()):
         issues.append(WalkForwardValidationIssue(severity="ERROR", message="Live execution artifacts found"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return WalkForwardValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_walk_forward_run_result(result: WalkForwardRunResult) -> WalkForwardValidationReport:
    req_report = validate_walk_forward_run_request(result.request)
    win_report = validate_walk_forward_windows(result.windows)
    opt_report = validate_no_walk_forward_optimization(result)

    issues = req_report.issues + win_report.issues + opt_report.issues

    if not result.window_results:
        issues.append(WalkForwardValidationIssue(severity="WARNING", message="No window results generated"))

    errors = [i.message for i in issues if i.severity == "ERROR"]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return WalkForwardValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def walk_forward_validation_report_to_text(report: WalkForwardValidationReport) -> str:
    lines = []
    lines.append("Walk-Forward Validation Report")
    lines.append(f"  Valid:    {report.valid}")
    lines.append(f"  Errors:   {report.error_count}")
    lines.append(f"  Warnings: {report.warning_count}")

    if report.errors:
        lines.append("\nErrors:")
        for err in report.errors:
            lines.append(f"  - {err}")

    if report.warnings:
        lines.append("\nWarnings:")
        for warn in report.warnings:
            lines.append(f"  - {warn}")

    return "\n".join(lines)

def assert_walk_forward_valid(report: WalkForwardValidationReport) -> None:
    if not report.valid:
        raise WalkForwardValidationError(f"Walk-forward validation failed with {report.error_count} errors: {', '.join(report.errors)}")
