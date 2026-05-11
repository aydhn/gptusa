from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from usa_signal_bot.taskqueue.task_models import LocalTask, TaskQueuePlan, TaskQueueRunResult, WorkloadBudgetEvaluation, TaskConflict
from usa_signal_bot.core.exceptions import TaskQueueValidationError
import json

@dataclass
class TaskQueueValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskQueueValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[TaskQueueValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_local_task_report(task: LocalTask) -> TaskQueueValidationReport:
    issues = []
    if not task.name: issues.append(TaskQueueValidationIssue("ERROR", "name", "Task name cannot be empty"))
    if task.command:
        if "token" in task.command.lower() or "secret" in task.command.lower(): issues.append(TaskQueueValidationIssue("ERROR", "command", "Command may contain secrets"))
        if any(d in task.command for d in ["cleanup-execute", "rollback-execute", "send-broker-order", "live-order", "demo-order"]): issues.append(TaskQueueValidationIssue("BLOCKED", "command", "Destructive command detected"))
    return TaskQueueValidationReport(valid=(len([i for i in issues if i.severity in ("ERROR", "BLOCKED")]) == 0), issue_count=len(issues), warning_count=len([i for i in issues if i.severity == "WARNING"]), error_count=len([i for i in issues if i.severity == "ERROR"]), blocked_count=len([i for i in issues if i.severity == "BLOCKED"]), issues=issues, warnings=[i.message for i in issues if i.severity == "WARNING"], errors=[i.message for i in issues if i.severity in ("ERROR", "BLOCKED")])

def validate_task_queue_plan_report(plan: TaskQueuePlan) -> TaskQueueValidationReport:
    issues = []
    if any(c.blocking for c in plan.conflicts): issues.append(TaskQueueValidationIssue("BLOCKED", "conflicts", "Plan has blocking conflicts"))
    for task in plan.tasks:
        tr = validate_local_task_report(task)
        if not tr.valid: issues.append(TaskQueueValidationIssue("ERROR", f"task_{task.task_id}", f"Task validation failed: {tr.errors}"))
    if plan.budget_evaluation and plan.budget_evaluation.errors: issues.append(TaskQueueValidationIssue("ERROR", "budget", "Plan exceeds workload budget"))
    return TaskQueueValidationReport(valid=(len([i for i in issues if i.severity in ("ERROR", "BLOCKED")]) == 0), issue_count=len(issues), warning_count=len([i for i in issues if i.severity == "WARNING"]), error_count=len([i for i in issues if i.severity == "ERROR"]), blocked_count=len([i for i in issues if i.severity == "BLOCKED"]), issues=issues, warnings=[i.message for i in issues if i.severity == "WARNING"], errors=[i.message for i in issues if i.severity in ("ERROR", "BLOCKED")])

def validate_task_queue_run_result_report(result: TaskQueueRunResult) -> TaskQueueValidationReport:
    issues = []
    if result.status.value in ["BLOCKED", "FAILED"]: issues.append(TaskQueueValidationIssue("ERROR", "status", f"Run failed or blocked: {result.status.value}"))
    if not validate_task_queue_plan_report(result.plan).valid: issues.append(TaskQueueValidationIssue("ERROR", "plan", "Underlying plan is invalid"))
    return TaskQueueValidationReport(valid=(len([i for i in issues if i.severity == "ERROR"]) == 0), issue_count=len(issues), warning_count=0, error_count=len([i for i in issues if i.severity == "ERROR"]), blocked_count=0, issues=issues, warnings=[], errors=[i.message for i in issues])

def validate_workload_budget_evaluation_report(evaluation: WorkloadBudgetEvaluation) -> TaskQueueValidationReport:
    issues = []
    for e in evaluation.errors: issues.append(TaskQueueValidationIssue("ERROR", "budget", e))
    for w in evaluation.warnings: issues.append(TaskQueueValidationIssue("WARNING", "budget", w))
    return TaskQueueValidationReport(valid=(len(evaluation.errors) == 0), issue_count=len(issues), warning_count=len(evaluation.warnings), error_count=len(evaluation.errors), blocked_count=0, issues=issues, warnings=evaluation.warnings, errors=evaluation.errors)

def validate_task_conflicts_report(conflicts: List[TaskConflict]) -> TaskQueueValidationReport:
    issues = [TaskQueueValidationIssue("BLOCKED" if c.blocking else "WARNING", "conflict", c.message) for c in conflicts]
    return TaskQueueValidationReport(valid=(len([i for i in issues if i.severity in ("ERROR", "BLOCKED")]) == 0), issue_count=len(issues), warning_count=len([i for i in issues if i.severity == "WARNING"]), error_count=0, blocked_count=len([i for i in issues if i.severity == "BLOCKED"]), issues=issues, warnings=[i.message for i in issues if i.severity == "WARNING"], errors=[i.message for i in issues if i.severity in ("ERROR", "BLOCKED")])

def validate_no_destructive_tasks(tasks: List[LocalTask]) -> TaskQueueValidationReport:
    issues = [TaskQueueValidationIssue("BLOCKED", "command", f"Destructive task: {t.command}") for t in tasks if t.command and any(d in t.command for d in ["cleanup-execute", "rollback-execute", "send-broker-order", "live-order", "demo-order"])]
    return TaskQueueValidationReport(valid=(len(issues) == 0), issue_count=len(issues), warning_count=0, error_count=0, blocked_count=len(issues), issues=issues, warnings=[], errors=[i.message for i in issues])

def validate_no_sensitive_data_in_taskqueue_payload(payload: Dict[str, Any]) -> TaskQueueValidationReport:
    text = json.dumps(payload).lower()
    issues = [TaskQueueValidationIssue("ERROR", "payload", "Payload may contain sensitive data")] if any(k in text for k in ["api_key", "token", "secret", "password"]) else []
    return TaskQueueValidationReport(valid=(len(issues) == 0), issue_count=len(issues), warning_count=0, error_count=len(issues), blocked_count=0, issues=issues, warnings=[], errors=[i.message for i in issues])

def validate_no_live_execution_language_in_taskqueue(text: str) -> TaskQueueValidationReport:
    issues = [TaskQueueValidationIssue("ERROR", "text", f"Forbidden language used: {f}") for f in ["kesin al", "garanti", "live approved", "yatirim tavsiyesi", "investment advice"] if f in text.lower()]
    return TaskQueueValidationReport(valid=(len(issues) == 0), issue_count=len(issues), warning_count=0, error_count=len(issues), blocked_count=0, issues=issues, warnings=[], errors=[i.message for i in issues])

def taskqueue_validation_report_to_text(report: TaskQueueValidationReport) -> str:
    return "\n".join(["Task Queue Validation Report", f"Valid: {report.valid}", f"Issues: {report.issue_count} (W:{report.warning_count} E:{report.error_count} B:{report.blocked_count})", "-" * 30] + [f"[{i.severity}] {i.field}: {i.message}" for i in report.issues])

def assert_taskqueue_valid(report: TaskQueueValidationReport) -> None:
    if not report.valid: raise TaskQueueValidationError(f"Task Queue validation failed: {report.errors}")
