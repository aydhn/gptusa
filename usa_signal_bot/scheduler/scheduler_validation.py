from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.scheduler.scheduler_models import RunLock, ConcurrencyPolicy, SchedulerPlan, SchedulerRunResult
from usa_signal_bot.scheduler.stale_lock_detector import StaleLockReport
from usa_signal_bot.core.exceptions import SchedulerValidationError

@dataclass
class SchedulerValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SchedulerValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[SchedulerValidationIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def _add_issue(report: SchedulerValidationReport, severity: str, field_name: Optional[str], msg: str):
    report.issues.append(SchedulerValidationIssue(severity=severity, field=field_name, message=msg))
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
    report.issue_count += 1

def validate_run_lock_report(lock: RunLock) -> SchedulerValidationReport:
    report = SchedulerValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    if not lock.lock_path:
        _add_issue(report, "ERROR", "lock_path", "lock_path cannot be empty")
    if lock.stale_after_seconds <= 0:
        _add_issue(report, "ERROR", "stale_after_seconds", "stale_after_seconds must be positive")
    return report

def validate_concurrency_policy_report(policy: ConcurrencyPolicy) -> SchedulerValidationReport:
    report = SchedulerValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    if policy.max_concurrent_runs <= 0:
        _add_issue(report, "ERROR", "max_concurrent_runs", "must be positive")
    if policy.wait_timeout_seconds < 0:
        _add_issue(report, "ERROR", "wait_timeout_seconds", "cannot be negative")
    return report

def validate_no_destructive_scheduler_jobs(plan: SchedulerPlan) -> SchedulerValidationReport:
    report = SchedulerValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    forbidden = ["cleanup-execute", "rollback-execute", "send-broker-order", "live-order", "demo-order"]
    for j in plan.jobs:
        if j.command:
            low_cmd = j.command.lower()
            for f in forbidden:
                if f in low_cmd:
                    _add_issue(report, "BLOCKED", f"job.{j.name}.command", f"Contains forbidden command: {f}")
    return report

def validate_no_sensitive_data_in_scheduler_payload(payload: Dict[str, Any]) -> SchedulerValidationReport:
    report = SchedulerValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    s_payload = str(payload).lower()
    if "secret" in s_payload or "token" in s_payload or "api_key" in s_payload:
        _add_issue(report, "BLOCKED", "payload", "Potentially sensitive data found in payload")
    return report

def validate_no_live_execution_language_in_scheduler(text: str) -> SchedulerValidationReport:
    report = SchedulerValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    bad_phrases = ["live approved", "sent to broker", "kesin al", "garanti", "investment advice"]
    low = text.lower()
    for b in bad_phrases:
        if b in low:
            _add_issue(report, "BLOCKED", "text", f"Contains forbidden live execution language: {b}")
    return report

def validate_scheduler_plan_report(plan: SchedulerPlan) -> SchedulerValidationReport:
    report = validate_no_destructive_scheduler_jobs(plan)
    return report

def validate_scheduler_run_result_report(result: SchedulerRunResult) -> SchedulerValidationReport:
    report = validate_scheduler_plan_report(result.plan)
    return report

def validate_stale_lock_report_report(report: StaleLockReport) -> SchedulerValidationReport:
    res = SchedulerValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0)
    # Stale locks are just facts, no explicit validation failures usually
    return res

def scheduler_validation_report_to_text(report: SchedulerValidationReport) -> str:
    lines = [f"Scheduler Validation: {'PASS' if report.valid else 'FAIL'}"]
    if report.issues:
        lines.append(f"Issues ({report.issue_count}):")
        for i in report.issues:
            lines.append(f"  - [{i.severity}] {i.field or 'general'}: {i.message}")
    return "\n".join(lines)

def assert_scheduler_valid(report: SchedulerValidationReport) -> None:
    if not report.valid:
        raise SchedulerValidationError(f"Scheduler validation failed with {report.error_count} errors and {report.blocked_count} blocked issues.")
