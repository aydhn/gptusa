from dataclasses import dataclass, field
from typing import Any, Dict, List

from usa_signal_bot.core.exceptions import RuntimeValidationError
from usa_signal_bot.runtime.runtime_models import (
    MarketScanRequest, MarketScanResult, RuntimeState, PipelineStepResult, ScheduledScanPlan
)
from usa_signal_bot.core.enums import PipelineStepStatus, RuntimeRunStatus

@dataclass
class RuntimeValidationIssue:
    severity: str
    field: str | None
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: List[RuntimeValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[RuntimeValidationIssue]) -> RuntimeValidationReport:
    errors = [i.message for i in issues if i.severity == "error"]
    warnings = [i.message for i in issues if i.severity == "warning"]
    return RuntimeValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_market_scan_request_report(request: MarketScanRequest) -> RuntimeValidationReport:
    issues = []
    if not request.run_name:
        issues.append(RuntimeValidationIssue("error", "run_name", "run_name cannot be empty"))
    if not request.timeframes:
        issues.append(RuntimeValidationIssue("error", "timeframes", "timeframes cannot be empty"))
    if not request.provider_name:
        issues.append(RuntimeValidationIssue("error", "provider_name", "provider_name cannot be empty"))
    if request.max_symbols is not None and request.max_symbols <= 0:
        issues.append(RuntimeValidationIssue("error", "max_symbols", "max_symbols must be None or positive"))
    return _create_report(issues)

def validate_market_scan_result(result: MarketScanResult) -> RuntimeValidationReport:
    issues = []
    issues.extend(validate_market_scan_request_report(result.request).issues)
    issues.extend(validate_no_live_execution_in_scan(result).issues)
    issues.extend(validate_pipeline_step_results(result.step_results).issues)
    return _create_report(issues)

def validate_runtime_state(state: RuntimeState) -> RuntimeValidationReport:
    issues = []
    if not state.run_id:
        issues.append(RuntimeValidationIssue("error", "run_id", "run_id cannot be empty"))
    return _create_report(issues)

def validate_pipeline_step_results(results: List[PipelineStepResult]) -> RuntimeValidationReport:
    issues = []
    for r in results:
        if r.duration_seconds is not None and r.duration_seconds < 0:
            issues.append(RuntimeValidationIssue("error", f"duration_seconds_{r.step_name}", "Duration cannot be negative"))
    return _create_report(issues)

def validate_no_live_execution_in_scan(result: MarketScanResult) -> RuntimeValidationReport:
    issues = []
    # Ensure no live execution data exists in any part of the metadata/summary
    if result.request.metadata.get("live_order") or result.request.metadata.get("broker_order"):
        issues.append(RuntimeValidationIssue("error", "request", "Live/Broker order flag found in request"))
    for r in result.step_results:
        if "broker_order" in r.summary or "live_order" in r.summary or "paper_order" in r.summary:
            issues.append(RuntimeValidationIssue("error", f"step_{r.step_name}", "Order generation detected in scan"))
        if "telegram_sent" in r.summary:
            issues.append(RuntimeValidationIssue("error", f"step_{r.step_name}", "Telegram sending detected in scan"))
    return _create_report(issues)

def validate_scheduled_scan_plan_report(plan: ScheduledScanPlan) -> RuntimeValidationReport:
    issues = []
    if plan.interval_minutes <= 0:
        issues.append(RuntimeValidationIssue("error", "interval_minutes", "interval_minutes must be positive"))
    if plan.max_runs_per_day <= 0:
        issues.append(RuntimeValidationIssue("error", "max_runs_per_day", "max_runs_per_day must be positive"))
    issues.extend(validate_market_scan_request_report(plan.scan_request_template).issues)
    return _create_report(issues)

def runtime_validation_report_to_text(report: RuntimeValidationReport) -> str:
    lines = [f"Valid: {report.valid}"]
    for issue in report.issues:
        lines.append(f"[{issue.severity.upper()}] {issue.field}: {issue.message}")
    return "\n".join(lines)

def assert_runtime_valid(report: RuntimeValidationReport) -> None:
    if not report.valid:
        raise RuntimeValidationError("Runtime validation failed:\n" + runtime_validation_report_to_text(report))
