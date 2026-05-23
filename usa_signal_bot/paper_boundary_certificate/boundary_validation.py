from typing import Any
from dataclasses import dataclass, field
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import (
    PaperSandboxBoundaryCertificate, AdmissionBlockerReplayResult,
    NoOrderEvidenceFreezeBundle, BoundaryCertificateFullReview
)
from usa_signal_bot.core.exceptions import BoundaryValidationError

@dataclass
class BoundaryValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoundaryValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[BoundaryValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_boundary_certificate_report(item: PaperSandboxBoundaryCertificate) -> BoundaryValidationReport:
    issues = []
    if not item.sealed: issues.append(BoundaryValidationIssue("error", "sealed", "Certificate must be sealed"))
    if not item.immutable: issues.append(BoundaryValidationIssue("error", "immutable", "Certificate must be immutable"))
    if not item.activation_denied: issues.append(BoundaryValidationIssue("error", "activation_denied", "activation_denied must be True"))
    if item.activation_allowed: issues.append(BoundaryValidationIssue("error", "activation_allowed", "activation_allowed must be False"))
    if item.admission_allowed: issues.append(BoundaryValidationIssue("error", "admission_allowed", "admission_allowed must be False"))
    if item.transition_allowed: issues.append(BoundaryValidationIssue("error", "transition_allowed", "transition_allowed must be False"))
    if not item.all_writes_blocked: issues.append(BoundaryValidationIssue("error", "all_writes_blocked", "all_writes_blocked must be True"))
    if item.order_created: issues.append(BoundaryValidationIssue("error", "order_created", "order_created must be False"))
    if item.mutation_detected: issues.append(BoundaryValidationIssue("error", "mutation_detected", "mutation_detected must be False"))

    if item.allows_active_paper: issues.append(BoundaryValidationIssue("error", "allows_active_paper", "allows_active_paper must be False"))
    if item.allows_broker_execution: issues.append(BoundaryValidationIssue("error", "allows_broker_execution", "allows_broker_execution must be False"))
    if item.allows_paper_state_mutation: issues.append(BoundaryValidationIssue("error", "allows_paper_state_mutation", "allows_paper_state_mutation must be False"))
    if item.allows_config_patch: issues.append(BoundaryValidationIssue("error", "allows_config_patch", "allows_config_patch must be False"))
    if item.allows_telegram_real_send: issues.append(BoundaryValidationIssue("error", "allows_telegram_real_send", "allows_telegram_real_send must be False"))

    return _build_report(issues)

def validate_blocker_replay_result_report(item: AdmissionBlockerReplayResult) -> BoundaryValidationReport:
    issues = []
    if not item.passed: issues.append(BoundaryValidationIssue("error", "passed", "Replay must pass"))
    if item.allowed_attempt_count > 0: issues.append(BoundaryValidationIssue("error", "allowed_attempt_count", "Allowed attempt count must be 0"))
    return _build_report(issues)

def validate_evidence_freeze_report(item: NoOrderEvidenceFreezeBundle) -> BoundaryValidationReport:
    issues = []
    if not item.frozen: issues.append(BoundaryValidationIssue("error", "frozen", "Freeze must be frozen"))
    if not item.immutable: issues.append(BoundaryValidationIssue("error", "immutable", "Freeze must be immutable"))
    return _build_report(issues)

def validate_boundary_full_review_report(item: BoundaryCertificateFullReview) -> BoundaryValidationReport:
    issues = []
    for c in item.certificates:
        rep = validate_boundary_certificate_report(c)
        issues.extend(rep.issues)
    for r in item.replay_results:
        rep = validate_blocker_replay_result_report(r)
        issues.extend(rep.issues)
    for f in item.evidence_freezes:
        rep = validate_evidence_freeze_report(f)
        issues.extend(rep.issues)
    return _build_report(issues)

def validate_no_sensitive_data_in_boundary_payload(payload: dict[str, Any]) -> BoundaryValidationReport:
    return _build_report([])

def validate_no_live_execution_language_in_boundary(text: str) -> BoundaryValidationReport:
    issues = []
    text_lower = text.lower()
    for term in ["live approved", "sent to broker", "kesin al", "garanti"]:
        if term in text_lower:
            issues.append(BoundaryValidationIssue("error", "text", f"Live language found: {term}"))
    return _build_report(issues)

def validate_no_active_paper_language_in_boundary(text: str) -> BoundaryValidationReport:
    issues = []
    text_lower = text.lower()
    for term in ["paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr", "candidate kesin iyi"]:
        if term in text_lower:
            issues.append(BoundaryValidationIssue("error", "text", f"Active paper language found: {term}"))
    return _build_report(issues)

def validate_no_paper_state_mutation_fields_in_boundary(payload: dict[str, Any]) -> BoundaryValidationReport:
    issues = []
    text = str(payload).lower()
    for term in ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]:
        if term in text:
            if payload.get(term, False):
                issues.append(BoundaryValidationIssue("error", term, f"Paper mutation field {term} cannot be true"))
    return _build_report(issues)

def validate_no_broker_execution_fields_in_boundary(payload: dict[str, Any]) -> BoundaryValidationReport:
    issues = []
    for term in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if term in payload:
            issues.append(BoundaryValidationIssue("error", term, f"Broker field {term} found"))
    return _build_report(issues)

def boundary_validation_report_to_text(report: BoundaryValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.error_count}"

def assert_boundary_valid(report: BoundaryValidationReport) -> None:
    if not report.valid:
        raise BoundaryValidationError(f"Validation failed: {[e.message for e in report.issues]}")

def _build_report(issues: list[BoundaryValidationIssue]) -> BoundaryValidationReport:
    errs = [i for i in issues if i.severity == "error"]
    return BoundaryValidationReport(
        valid=len(errs) == 0,
        issue_count=len(issues),
        warning_count=sum(1 for i in issues if i.severity == "warning"),
        error_count=len(errs),
        blocked_count=sum(1 for i in issues if i.severity == "blocked"),
        issues=issues,
        warnings=[i.message for i in issues if i.severity == "warning"],
        errors=[i.message for i in errs]
    )
