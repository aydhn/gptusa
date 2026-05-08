import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.exceptions import ObservabilityValidationError
from usa_signal_bot.observability.observability_models import (
    ObservabilityEvent, OperationalMetricsSnapshot, OperationalHealthReport, LogRotationResult
)

@dataclass
class ObservabilityValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ObservabilityValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ObservabilityValidationIssue]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def _build_report(issues: List[ObservabilityValidationIssue]) -> ObservabilityValidationReport:
    w = sum(1 for i in issues if i.severity == "warning")
    e = sum(1 for i in issues if i.severity == "error")
    b = sum(1 for i in issues if i.severity == "blocked")
    return ObservabilityValidationReport(
        valid=b == 0 and e == 0,
        issue_count=len(issues),
        warning_count=w,
        error_count=e,
        blocked_count=b,
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "warning"],
        errors=[i.message for i in issues if i.severity in ["error", "blocked"]]
    )

def validate_no_sensitive_data_in_observability_payload(payload: Dict[str, Any]) -> ObservabilityValidationReport:
    iss = []
    bad_keys = ["token", "secret", "password", "credential", "api_key"]
    for k in payload.keys():
        kl = str(k).lower()
        if any(bad in kl for bad in bad_keys):
            if payload[k] != "[REDACTED]":
                iss.append(ObservabilityValidationIssue("blocked", str(k), "Payload contains unredacted sensitive key"))
    return _build_report(iss)

def validate_no_live_execution_language_in_observability(text: str) -> ObservabilityValidationReport:
    iss = []
    tl = text.lower()
    bad = ["live approved", "sent to broker", "kesin al", "garanti"]
    for b in bad:
        if b in tl:
            iss.append(ObservabilityValidationIssue("blocked", None, f"Observability data contains forbidden language: {b}"))
    return _build_report(iss)

def validate_observability_event_report(event: ObservabilityEvent) -> ObservabilityValidationReport:
    iss = []
    if not event.source: iss.append(ObservabilityValidationIssue("error", "source", "Empty source"))
    if not event.message: iss.append(ObservabilityValidationIssue("error", "message", "Empty message"))

    r = validate_no_sensitive_data_in_observability_payload(event.payload)
    iss.extend(r.issues)

    return _build_report(iss)

def validate_operational_snapshot_report(snapshot: OperationalMetricsSnapshot) -> ObservabilityValidationReport:
    iss = []
    if not snapshot.metrics:
        iss.append(ObservabilityValidationIssue("warning", "metrics", "Snapshot has no metrics"))
    return _build_report(iss)

def validate_operational_health_report_report(report: OperationalHealthReport) -> ObservabilityValidationReport:
    iss = []
    if report.status.value == "HEALTHY" and report.error_count > 0:
        iss.append(ObservabilityValidationIssue("warning", "status", "Report is healthy but has errors"))
    return _build_report(iss)

def validate_log_rotation_result_report(result: LogRotationResult) -> ObservabilityValidationReport:
    iss = []
    if result.status.value == "ROTATED" and not result.rotated_path:
        iss.append(ObservabilityValidationIssue("error", "rotated_path", "Rotated status but missing rotated path"))
    return _build_report(iss)

def observability_validation_report_to_text(report: ObservabilityValidationReport) -> str:
    lines = [f"Validation Valid: {report.valid}"]
    for i in report.issues:
        lines.append(f"  - [{i.severity.upper()}] {i.field}: {i.message}")
    return "\n".join(lines)

def assert_observability_valid(report: ObservabilityValidationReport) -> None:
    if not report.valid:
        raise ObservabilityValidationError(f"Observability validation failed: {report.errors}")
