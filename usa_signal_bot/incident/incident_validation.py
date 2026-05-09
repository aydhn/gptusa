from dataclasses import dataclass, field
from typing import Any
import json
from usa_signal_bot.core.enums import IncidentStatus, RecoveryPlanStatus, RollbackPlanStatus, RollbackSafetyStatus
from usa_signal_bot.incident.incident_models import IncidentSummaryReport, incident_summary_report_to_dict
from usa_signal_bot.incident.recovery_models import RecoveryPlan, RecoveryPlanResult, recovery_plan_to_dict, recovery_plan_result_to_dict
from usa_signal_bot.incident.rollback_models import RollbackPlan, RollbackExecutionResult, rollback_plan_to_dict, rollback_execution_result_to_dict
from usa_signal_bot.incident.rollback_precheck import RollbackPrecheckReport, rollback_precheck_report_to_dict
from usa_signal_bot.core.exceptions import IncidentValidationError

@dataclass
class IncidentValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class IncidentValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[IncidentValidationIssue]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def _validate_payload_str(payload: str) -> list[IncidentValidationIssue]:
    issues = []
    p = payload.lower()
    for term in ["secret", "token", "password", "api_key", "credential"]:
        if term in p and "redacted" not in p:
             issues.append(IncidentValidationIssue("BLOCKED", "payload", f"Payload may contain sensitive token: {term}"))
    for term in ["investment advice", "live approval", "live trade", "live order", "kesin al", "garanti", "sent to broker", "live approved"]:
        if term in p and "not " not in p and "no " not in p:
             issues.append(IncidentValidationIssue("BLOCKED", "language", f"Prohibited language found: {term}"))
    return issues

def validate_no_sensitive_data_in_incident_payload(payload: dict[str, Any]) -> IncidentValidationReport:
    issues = _validate_payload_str(json.dumps(payload))
    valid = not any(i.severity == "BLOCKED" for i in issues)
    return IncidentValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=sum(1 for i in issues if i.severity == "BLOCKED"),
        issues=issues
    )

def validate_no_live_execution_language_in_incident(text: str) -> IncidentValidationReport:
    issues = _validate_payload_str(text)
    valid = not any(i.severity == "BLOCKED" for i in issues)
    return IncidentValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=sum(1 for i in issues if i.severity == "BLOCKED"),
        issues=issues
    )

def validate_no_protected_overwrite_in_rollback(plan: RollbackPlan) -> IncidentValidationReport:
    issues = []
    if not plan.dry_run:
        for s in plan.steps:
            if s.protected:
                issues.append(IncidentValidationIssue("BLOCKED", s.target_path, "Protected overwrite attempted in non-dry-run plan."))
    valid = not any(i.severity == "BLOCKED" for i in issues)
    return IncidentValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=sum(1 for i in issues if i.severity == "BLOCKED"),
        issues=issues
    )

def validate_incident_report_report(report: IncidentSummaryReport) -> IncidentValidationReport:
    rep1 = validate_no_sensitive_data_in_incident_payload(incident_summary_report_to_dict(report))
    return rep1

def validate_recovery_plan_report(plan: RecoveryPlan) -> IncidentValidationReport:
    issues = []
    if not plan.dry_run:
        issues.append(IncidentValidationIssue("WARNING", "dry_run", "Recovery plan execute commands is true."))
    rep1 = validate_no_sensitive_data_in_incident_payload(recovery_plan_to_dict(plan))
    issues.extend(rep1.issues)
    valid = not any(i.severity == "BLOCKED" for i in issues)
    return IncidentValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=sum(1 for i in issues if i.severity == "WARNING"),
        error_count=0,
        blocked_count=sum(1 for i in issues if i.severity == "BLOCKED"),
        issues=issues
    )

def validate_recovery_result_report(result: RecoveryPlanResult) -> IncidentValidationReport:
    rep1 = validate_no_sensitive_data_in_incident_payload(recovery_plan_result_to_dict(result))
    return rep1

def validate_rollback_plan_report(plan: RollbackPlan) -> IncidentValidationReport:
    rep1 = validate_no_protected_overwrite_in_rollback(plan)
    rep2 = validate_no_sensitive_data_in_incident_payload(rollback_plan_to_dict(plan))
    issues = rep1.issues + rep2.issues
    valid = not any(i.severity == "BLOCKED" for i in issues)
    return IncidentValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=sum(1 for i in issues if i.severity == "BLOCKED"),
        issues=issues
    )

def validate_rollback_result_report(result: RollbackExecutionResult) -> IncidentValidationReport:
    issues = []
    if result.dry_run:
        if result.executed_steps:
             issues.append(IncidentValidationIssue("BLOCKED", "executed_steps", "Dry-run result contains executed steps."))

    rep1 = validate_no_protected_overwrite_in_rollback(result.plan)
    issues.extend(rep1.issues)

    valid = not any(i.severity == "BLOCKED" for i in issues)
    return IncidentValidationReport(
        valid=valid,
        issue_count=len(issues),
        warning_count=0,
        error_count=0,
        blocked_count=sum(1 for i in issues if i.severity == "BLOCKED"),
        issues=issues
    )

def validate_rollback_precheck_report_report(report: RollbackPrecheckReport) -> IncidentValidationReport:
    return validate_no_sensitive_data_in_incident_payload(rollback_precheck_report_to_dict(report))

def incident_validation_report_to_text(report: IncidentValidationReport) -> str:
    lines = [f"Valid: {report.valid}"]
    for i in report.issues:
        lines.append(f"  [{i.severity}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_incident_valid(report: IncidentValidationReport) -> None:
    if not report.valid:
        raise IncidentValidationError("Incident validation failed. See issues.\n" + incident_validation_report_to_text(report))
