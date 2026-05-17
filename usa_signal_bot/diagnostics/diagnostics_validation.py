import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, FailureCluster, StrategyDiagnosticResult,
    RemediationHint, DiagnosticScorecard, DiagnosticReview
)
from usa_signal_bot.core.exceptions import DiagnosticsValidationError

@dataclass
class DiagnosticsValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DiagnosticsValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[DiagnosticsValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_diagnostic_events_report(items: List[DiagnosticEvent]) -> DiagnosticsValidationReport:
    # Placeholder
    return DiagnosticsValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_failure_assessments_report(items: List[FailureModeAssessment]) -> DiagnosticsValidationReport:
    return DiagnosticsValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_failure_clusters_report(items: List[FailureCluster]) -> DiagnosticsValidationReport:
    return DiagnosticsValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_strategy_diagnostics_report(items: List[StrategyDiagnosticResult]) -> DiagnosticsValidationReport:
    return DiagnosticsValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_remediation_hints_report(items: List[RemediationHint]) -> DiagnosticsValidationReport:
    return DiagnosticsValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_diagnostic_scorecard_report(item: DiagnosticScorecard) -> DiagnosticsValidationReport:
    return DiagnosticsValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_diagnostics(text: str) -> DiagnosticsValidationReport:
    lower_text = text.lower()
    bad_phrases = ["live approved", "sent to broker", "kesin al", "garanti"]
    errors = []
    for bp in bad_phrases:
        if bp in lower_text:
            errors.append(f"Found forbidden live execution language: '{bp}'")

    return DiagnosticsValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=[DiagnosticsValidationIssue("CRITICAL", None, e) for e in errors],
        warnings=[],
        errors=errors
    )

def validate_no_broker_execution_fields_in_diagnostics(payload: Dict[str, Any]) -> DiagnosticsValidationReport:
    text = json.dumps(payload).lower()
    bad_fields = ["broker_order_id", "live_order_id", "real_fill_id", "alpaca", "ibkr"]
    errors = []
    for bf in bad_fields:
        if bf in text:
            errors.append(f"Found forbidden broker field in payload: '{bf}'")

    return DiagnosticsValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=[DiagnosticsValidationIssue("CRITICAL", None, e) for e in errors],
        warnings=[],
        errors=errors
    )

def validate_no_auto_optimization_language_in_diagnostics(text: str) -> DiagnosticsValidationReport:
    lower_text = text.lower()
    bad_phrases = ["bu strateji kesin bozuk", "kesin kapat", "otomatik optimize et", "kesin kâr"]
    errors = []
    for bp in bad_phrases:
        if bp in lower_text:
            errors.append(f"Found forbidden auto-optimization or certainty language: '{bp}'")

    return DiagnosticsValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=[DiagnosticsValidationIssue("CRITICAL", None, e) for e in errors],
        warnings=[],
        errors=errors
    )

def validate_no_sensitive_data_in_diagnostics_payload(payload: Dict[str, Any]) -> DiagnosticsValidationReport:
    text = json.dumps(payload).lower()
    bad_words = ["secret", "token", "password", "api_key"]
    errors = []
    for bw in bad_words:
        if f'"{bw}"' in text or f"'{bw}'" in text:
            errors.append(f"Found potential sensitive data field in payload: '{bw}'")

    return DiagnosticsValidationReport(
        valid=len(errors) == 0,
        issue_count=len(errors),
        warning_count=0,
        error_count=len(errors),
        blocked_count=len(errors),
        issues=[DiagnosticsValidationIssue("CRITICAL", None, e) for e in errors],
        warnings=[],
        errors=errors
    )

def validate_diagnostic_review_report(item: DiagnosticReview) -> DiagnosticsValidationReport:
    from usa_signal_bot.diagnostics.diagnostic_models import diagnostic_review_to_dict
    payload = diagnostic_review_to_dict(item)
    text = json.dumps(payload)

    r1 = validate_no_live_execution_language_in_diagnostics(text)
    r2 = validate_no_broker_execution_fields_in_diagnostics(payload)
    r3 = validate_no_auto_optimization_language_in_diagnostics(text)
    r4 = validate_no_sensitive_data_in_diagnostics_payload(payload)

    all_errors = r1.errors + r2.errors + r3.errors + r4.errors

    return DiagnosticsValidationReport(
        valid=len(all_errors) == 0,
        issue_count=len(all_errors),
        warning_count=0,
        error_count=len(all_errors),
        blocked_count=len(all_errors),
        issues=r1.issues + r2.issues + r3.issues + r4.issues,
        warnings=[],
        errors=all_errors
    )

def diagnostics_validation_report_to_text(report: DiagnosticsValidationReport) -> str:
    lines = [
        f"Diagnostics Validation Report: {'VALID' if report.valid else 'INVALID'}",
        f"  Errors: {report.error_count}"
    ]
    for e in report.errors:
        lines.append(f"  - {e}")
    return "\n".join(lines)

def assert_diagnostics_valid(report: DiagnosticsValidationReport) -> None:
    if not report.valid:
        raise DiagnosticsValidationError(f"Diagnostics validation failed: {report.errors}")
