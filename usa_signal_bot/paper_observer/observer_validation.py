from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_observer.observer_models import (
    PaperObserverEnrollment, ObserverRuntimeContext, ObserverRuntimeSession, PaperObserverReview
)

@dataclass
class ObserverValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ObserverValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[ObserverValidationIssue]) -> ObserverValidationReport:
    warnings = [i for i in issues if i.severity == "WARNING"]
    errors = [i for i in issues if i.severity == "ERROR"]
    blocked = [i for i in issues if i.severity == "BLOCKED"]
    return ObserverValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=[w.message for w in warnings],
        errors=[e.message for e in errors] + [b.message for b in blocked]
    )

def validate_observer_enrollment_report(item: PaperObserverEnrollment) -> ObserverValidationReport:
    issues = []
    if item.allowed_for_active_paper:
        issues.append(ObserverValidationIssue("BLOCKED", "allowed_for_active_paper", "Enrollment cannot allow active paper"))
    return _create_report(issues)

def validate_observer_context_report(item: ObserverRuntimeContext) -> ObserverValidationReport:
    issues = []
    if not item.locked:
        issues.append(ObserverValidationIssue("BLOCKED", "locked", "Context must be locked"))
    return _create_report(issues)

def validate_observer_session_report(item: ObserverRuntimeSession) -> ObserverValidationReport:
    issues = []
    for out in item.outputs:
        if out.is_real_order:
            issues.append(ObserverValidationIssue("BLOCKED", "is_real_order", f"Output {out.output_id} is real order"))
    return _create_report(issues)

def validate_paper_observer_review_report(item: PaperObserverReview) -> ObserverValidationReport:
    issues = []
    for enr in item.enrollments:
        rep = validate_observer_enrollment_report(enr)
        issues.extend(rep.issues)
    for sess in item.sessions:
        rep = validate_observer_session_report(sess)
        issues.extend(rep.issues)
    return _create_report(issues)

def validate_no_sensitive_data_in_observer_payload(payload: Dict[str, Any]) -> ObserverValidationReport:
    issues = []
    s = str(payload).lower()
    for word in ["secret", "api_key", "token", "password"]:
        if word in s and "***redacted***" not in s:
            issues.append(ObserverValidationIssue("ERROR", "payload", f"Possible leak of {word}"))
    return _create_report(issues)

def validate_no_live_execution_language_in_observer(text: str) -> ObserverValidationReport:
    issues = []
    for w in ["live approved", "sent to broker", "kesin al", "garanti", "gerçek emir"]:
        if w in text.lower():
            issues.append(ObserverValidationIssue("BLOCKED", "text", f"Contains execution language: {w}"))
    return _create_report(issues)

def validate_no_active_paper_language_in_observer(text: str) -> ObserverValidationReport:
    issues = []
    for w in ["paper'a uygula", "canlıya al", "aktif et", "candidate kesin iyi"]:
        if w in text.lower():
            issues.append(ObserverValidationIssue("BLOCKED", "text", f"Contains active paper language: {w}"))
    return _create_report(issues)

def validate_no_paper_state_mutation_fields_in_observer(payload: Dict[str, Any]) -> ObserverValidationReport:
    issues = []
    for f in ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]:
        if payload.get(f) is True:
            issues.append(ObserverValidationIssue("BLOCKED", f, f"Payload has {f}=True"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_observer(payload: Dict[str, Any]) -> ObserverValidationReport:
    issues = []
    for f in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if f in payload:
            issues.append(ObserverValidationIssue("BLOCKED", f, f"Payload has {f}"))
    return _create_report(issues)

def observer_validation_report_to_text(report: ObserverValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}, Blocked: {report.blocked_count}"

def assert_observer_valid(report: ObserverValidationReport) -> None:
    from usa_signal_bot.core.exceptions import ObserverValidationError
    if not report.valid:
        raise ObserverValidationError(f"Validation failed: {report.errors}")
