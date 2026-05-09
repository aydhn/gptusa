from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.retention.retention_models import (
    RetentionPolicy, CleanupPlan, CleanupExecutionResult, DiskQuotaReport
)
from usa_signal_bot.core.enums import CleanupCandidateStatus

@dataclass
class RetentionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class RetentionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[RetentionValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_retention_policies_report(policies: list[RetentionPolicy]) -> RetentionValidationReport:
    issues = []
    for p in policies:
        if p.keep_latest < 0:
            issues.append(RetentionValidationIssue("ERROR", "keep_latest", f"Policy {p.name} has negative keep_latest"))
        if p.action.value == "DELETE" and p.protected:
            issues.append(RetentionValidationIssue("BLOCKED", "action", f"Policy {p.name} is protected but has DELETE action"))

    return _build_report(issues)

def validate_cleanup_plan_report(plan: CleanupPlan) -> RetentionValidationReport:
    issues = []
    for c in plan.candidates:
        if c.status == CleanupCandidateStatus.PROTECTED and c.recommended_action.value == "DELETE":
             issues.append(RetentionValidationIssue("BLOCKED", "status", f"Protected path marked for deletion: {c.path}"))

        path_str = c.path.lower()
        if c.status == CleanupCandidateStatus.CANDIDATE and any(x in path_str for x in ["usa_signal_bot", "config", "tests", "docs"]):
             issues.append(RetentionValidationIssue("BLOCKED", "path", f"Source/config marked as candidate for deletion: {c.path}"))

    return _build_report(issues)

def validate_cleanup_execution_result_report(result: CleanupExecutionResult) -> RetentionValidationReport:
    issues = []
    if result.dry_run and result.bytes_freed > 0:
        issues.append(RetentionValidationIssue("ERROR", "bytes_freed", "Dry run result claims to have freed > 0 bytes"))
    return _build_report(issues)

def validate_disk_quota_report_report(report: DiskQuotaReport) -> RetentionValidationReport:
    return _build_report([])

def validate_no_live_execution_language_in_retention(text: str) -> RetentionValidationReport:
    issues = []
    lower_text = text.lower()
    for phrase in ["live approved", "kesin al", "garanti", "investment advice"]:
        if phrase in lower_text:
             issues.append(RetentionValidationIssue("BLOCKED", None, f"Found prohibited language: {phrase}"))
    return _build_report(issues)

def validate_no_sensitive_data_in_retention_payload(payload: dict[str, Any]) -> RetentionValidationReport:
    issues = []
    import json
    text = json.dumps(payload).lower()
    if "secret" in text or "token" in text:
         issues.append(RetentionValidationIssue("BLOCKED", None, "Potential secret/token found in payload"))
    return _build_report(issues)

def assert_retention_valid(report: RetentionValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Retention validation failed: {report.errors}")

def _build_report(issues: list[RetentionValidationIssue]) -> RetentionValidationReport:
    errors = [i.message for i in issues if i.severity in ("ERROR", "BLOCKED")]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    return RetentionValidationReport(
        valid=len([i for i in issues if i.severity == "BLOCKED"]) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "BLOCKED"]),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def retention_validation_report_to_text(report: RetentionValidationReport) -> str:
    lines = [f"Valid: {report.valid}", f"Issues: {report.issue_count} ({report.blocked_count} blocked)"]
    for i in report.issues:
        lines.append(f"- [{i.severity}] {i.field}: {i.message}")
    return "\n".join(lines)
