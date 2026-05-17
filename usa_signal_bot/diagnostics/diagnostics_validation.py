from typing import Any
from dataclasses import dataclass, field
import json

@dataclass
class DiagnosticsValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class DiagnosticsValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[DiagnosticsValidationIssue]
    warnings: list[str]
    errors: list[str]

def _create_report(issues: list[DiagnosticsValidationIssue]) -> DiagnosticsValidationReport:
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARNING"]
    blocked = [i for i in issues if i.severity == "BLOCKED"]
    return DiagnosticsValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=[i.message for i in warnings],
        errors=[i.message for i in errors + blocked]
    )

def validate_no_live_execution_language_in_diagnostics(text: str) -> DiagnosticsValidationReport:
    issues = []
    txt = text.lower()
    for bad in ["live approved", "sent to broker", "kesin al", "garanti"]:
        if bad in txt:
            issues.append(DiagnosticsValidationIssue("BLOCKED", "language", f"Live execution language detected: {bad}"))
    return _create_report(issues)

def validate_no_sensitive_data_in_diagnostics_payload(payload: dict[str, Any]) -> DiagnosticsValidationReport:
    issues = []
    txt = json.dumps(payload).lower()
    for secret in ["api_key", "secret", "token", "password"]:
        if secret in txt:
            issues.append(DiagnosticsValidationIssue("BLOCKED", "metadata", f"Potential secret leak: {secret}"))
    return _create_report(issues)
