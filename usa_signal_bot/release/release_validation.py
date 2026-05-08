from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Any, Optional
from usa_signal_bot.core.enums import ReleaseValidationStatus
from usa_signal_bot.release.release_models import ReleaseBuildResult, ReleaseManifest, OperatorRunbook
from usa_signal_bot.release.backup_restore import BackupResult, RestoreDryRunResult
from usa_signal_bot.release.config_profiles import ConfigProfileValidationResult

@dataclass
class ReleaseValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict = field(default_factory=dict)

@dataclass
class ReleaseValidationReport:
    valid: bool
    status: ReleaseValidationStatus
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ReleaseValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_release_build_result_report(result: ReleaseBuildResult) -> ReleaseValidationReport:
    issues = []

    if result.request.include_secrets:
        issues.append(ReleaseValidationIssue("BLOCKED", "include_secrets", "Secrets inclusion must be disabled."))

    if result.status.value != "BUILT":
        issues.append(ReleaseValidationIssue("ERROR", "status", f"Build failed with status {result.status.value}"))

    if not result.bundle_path:
        issues.append(ReleaseValidationIssue("ERROR", "bundle_path", "Missing bundle path"))

    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    warnings = [i.message for i in issues if i.severity == "WARNING"]

    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.BLOCKED if any(i.severity == "BLOCKED" for i in issues) else (
               ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED),
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=sum(1 for i in issues if i.severity == "ERROR"),
        blocked_count=sum(1 for i in issues if i.severity == "BLOCKED"),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_release_manifest_report(manifest: ReleaseManifest) -> ReleaseValidationReport:
    issues = []
    if not manifest.artifacts:
        issues.append(ReleaseValidationIssue("WARNING", "artifacts", "No artifacts in manifest"))

    if not manifest.release_name:
        issues.append(ReleaseValidationIssue("ERROR", "release_name", "Missing release name"))

    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED,
        issue_count=len(issues), warning_count=len(warnings), error_count=len(errors), blocked_count=0,
        issues=issues, warnings=warnings, errors=errors
    )

def validate_release_bundle_file(bundle_path: Path, manifest: Optional[ReleaseManifest] = None) -> ReleaseValidationReport:
    # A dummy logic to represent file validation logic since LocalPackager does the real check.
    issues = []
    if not bundle_path.exists():
        issues.append(ReleaseValidationIssue("ERROR", "bundle_path", "Bundle file not found"))
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED,
        issue_count=len(issues), warning_count=0, error_count=len(errors), blocked_count=0,
        issues=issues, warnings=[], errors=errors
    )

def validate_operator_runbook_report(runbook: OperatorRunbook) -> ReleaseValidationReport:
    issues = []
    if "SAFETY_LIMITATIONS" not in runbook.sections:
        issues.append(ReleaseValidationIssue("WARNING", "sections", "Missing safety limitations section"))
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED,
        issue_count=len(issues), warning_count=len(warnings), error_count=len(errors), blocked_count=0,
        issues=issues, warnings=warnings, errors=errors
    )

def validate_backup_result_report(result: BackupResult) -> ReleaseValidationReport:
    issues = []
    if result.status.value != "CREATED":
        issues.append(ReleaseValidationIssue("ERROR", "status", "Backup creation failed"))
    if result.request.include_secrets:
        issues.append(ReleaseValidationIssue("BLOCKED", "include_secrets", "Secrets inclusion must be disabled"))
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED,
        issue_count=len(issues), warning_count=len(warnings), error_count=len(errors), blocked_count=0,
        issues=issues, warnings=warnings, errors=errors
    )

def validate_restore_dry_run_result_report(result: RestoreDryRunResult) -> ReleaseValidationReport:
    issues = []
    if result.status.value != "RESTORE_DRY_RUN_PASSED":
        issues.append(ReleaseValidationIssue("ERROR", "status", "Restore dry run failed"))
    if result.conflicts:
        issues.append(ReleaseValidationIssue("WARNING", "conflicts", f"Found {len(result.conflicts)} conflicts"))
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED,
        issue_count=len(issues), warning_count=len(warnings), error_count=len(errors), blocked_count=0,
        issues=issues, warnings=warnings, errors=errors
    )

def validate_config_profile_results(results: List[ConfigProfileValidationResult]) -> ReleaseValidationReport:
    issues = []
    for r in results:
        if r.status.value == "FAILED":
            issues.append(ReleaseValidationIssue("ERROR", "profile", f"Profile {r.name} failed: {r.errors}"))
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED,
        issue_count=len(issues), warning_count=0, error_count=len(errors), blocked_count=0,
        issues=issues, warnings=[], errors=errors
    )

def validate_no_secrets_in_release_payload(payload: dict) -> ReleaseValidationReport:
    issues = []
    if payload.get("include_secrets") is True:
        issues.append(ReleaseValidationIssue("BLOCKED", "payload", "include_secrets is explicitly true"))
    str_payload = str(payload).lower()
    if ".env" in str_payload or "secret=" in str_payload or "token=" in str_payload:
         issues.append(ReleaseValidationIssue("WARNING", "payload", "Potential secret string found in payload"))
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED,
        issue_count=len(issues), warning_count=0, error_count=len(errors), blocked_count=0,
        issues=issues, warnings=[], errors=errors
    )

def validate_no_live_execution_language_in_release(text: str) -> ReleaseValidationReport:
    issues = []
    lower = text.lower()
    dangerous_phrases = ["live approved", "kesin al", "kesin sat", "garanti", "investment advice"]
    for dp in dangerous_phrases:
        if dp in lower:
            issues.append(ReleaseValidationIssue("ERROR", "language", f"Dangerous language detected: '{dp}'"))
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    return ReleaseValidationReport(
        valid=len(errors) == 0,
        status=ReleaseValidationStatus.FAILED if errors else ReleaseValidationStatus.PASSED,
        issue_count=len(issues), warning_count=len(warnings), error_count=len(errors), blocked_count=0,
        issues=issues, warnings=warnings, errors=errors
    )

def release_validation_report_to_text(report: ReleaseValidationReport) -> str:
    lines = [f"Validation Status: {report.status.value}"]
    lines.append(f"Issues: {report.issue_count} (Blocked: {report.blocked_count}, Errors: {report.error_count}, Warnings: {report.warning_count})")
    for iss in report.issues:
        lines.append(f"- [{iss.severity}] {iss.field}: {iss.message}")
    return "\n".join(lines)

def assert_release_valid(report: ReleaseValidationReport) -> None:
    if not report.valid:
        from usa_signal_bot.core.exceptions import ReleaseValidationError
        raise ReleaseValidationError(f"Release validation failed: {report.errors}")
