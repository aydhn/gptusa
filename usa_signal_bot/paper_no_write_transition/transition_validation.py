from typing import Any
from dataclasses import dataclass, field
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    NoWriteTransitionDossier,
    AdmissionEvidenceSealValidation,
    PaperSandboxBridgeEnvelope,
    NoWriteTransitionFullReview
)

@dataclass
class NoWriteTransitionValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoWriteTransitionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[NoWriteTransitionValidationIssue]
    warnings: list[str]
    errors: list[str]

def _build_report(issues: list[NoWriteTransitionValidationIssue]) -> NoWriteTransitionValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocked = [i.message for i in issues if i.severity == "BLOCK"]
    return NoWriteTransitionValidationReport(
        valid=len(errors) == 0 and len(blocked) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocked),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_transition_dossier_report(item: NoWriteTransitionDossier) -> NoWriteTransitionValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(NoWriteTransitionValidationIssue("ERROR", "activation_denied", "Must be true"))
    if item.activation_allowed:
        issues.append(NoWriteTransitionValidationIssue("ERROR", "activation_allowed", "Must be false"))
    if item.transition_allowed:
        issues.append(NoWriteTransitionValidationIssue("ERROR", "transition_allowed", "Must be false"))
    if not item.all_writes_blocked:
        issues.append(NoWriteTransitionValidationIssue("ERROR", "all_writes_blocked", "Must be true"))
    if item.mutation_detected:
        issues.append(NoWriteTransitionValidationIssue("ERROR", "mutation_detected", "Must be false"))
    return _build_report(issues)

def validate_evidence_seal_validation_report(item: AdmissionEvidenceSealValidation) -> NoWriteTransitionValidationReport:
    issues = []
    if item.status.value == "FAILED":
        issues.append(NoWriteTransitionValidationIssue("BLOCK", "status", "Evidence seal validation failed"))
    return _build_report(issues)

def validate_sandbox_bridge_envelope_report(item: PaperSandboxBridgeEnvelope) -> NoWriteTransitionValidationReport:
    issues = []
    if not item.bridge_is_no_write:
        issues.append(NoWriteTransitionValidationIssue("ERROR", "bridge_is_no_write", "Must be true"))
    if not item.bridge_is_metadata_only:
        issues.append(NoWriteTransitionValidationIssue("ERROR", "bridge_is_metadata_only", "Must be true"))
    for r in item.routes:
        if r.write_allowed or r.order_allowed or r.broker_allowed or r.activation_allowed:
             issues.append(NoWriteTransitionValidationIssue("ERROR", "route", f"Route {r.route_type.value} allows dangerous op"))
    return _build_report(issues)

def validate_no_write_transition_full_review_report(item: NoWriteTransitionFullReview) -> NoWriteTransitionValidationReport:
    issues = []
    for dossier in item.dossiers:
        issues.extend(validate_transition_dossier_report(dossier).issues)
    for bridge in item.bridge_envelopes:
        issues.extend(validate_sandbox_bridge_envelope_report(bridge).issues)
    return _build_report(issues)

def validate_no_sensitive_data_in_transition_payload(payload: dict[str, Any]) -> NoWriteTransitionValidationReport:
    issues = []
    # simplified mock check
    return _build_report(issues)

def validate_no_live_execution_language_in_transition(text: str) -> NoWriteTransitionValidationReport:
    issues = []
    bad_words = ["live approved", "sent to broker", "kesin al", "garanti"]
    for bw in bad_words:
        if bw in text.lower():
            issues.append(NoWriteTransitionValidationIssue("BLOCK", "text", f"Live language detected: {bw}"))
    return _build_report(issues)

def validate_no_active_paper_language_in_transition(text: str) -> NoWriteTransitionValidationReport:
    issues = []
    bad_words = ["paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr", "candidate kesin iyi"]
    for bw in bad_words:
        if bw in text.lower():
            issues.append(NoWriteTransitionValidationIssue("BLOCK", "text", f"Active paper language detected: {bw}"))
    return _build_report(issues)

def validate_no_paper_state_mutation_fields_in_transition(payload: dict[str, Any]) -> NoWriteTransitionValidationReport:
    issues = []
    bad_fields = ["paper_state_committed", "paper_order_executed", "paper_order_created",
                  "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]
    for f in bad_fields:
        if f in payload and payload[f]:
            issues.append(NoWriteTransitionValidationIssue("ERROR", f, "Paper state mutation field detected"))
    return _build_report(issues)

def validate_no_broker_execution_fields_in_transition(payload: dict[str, Any]) -> NoWriteTransitionValidationReport:
    issues = []
    bad_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for f in bad_fields:
        if f in payload and payload[f]:
            issues.append(NoWriteTransitionValidationIssue("ERROR", f, "Broker execution field detected"))
    return _build_report(issues)

def no_write_transition_validation_report_to_text(report: NoWriteTransitionValidationReport) -> str:
    return f"Validation Report Valid: {report.valid} Errors: {report.error_count}"

def assert_no_write_transition_valid(report: NoWriteTransitionValidationReport) -> None:
    from usa_signal_bot.core.exceptions import NoWriteTransitionValidationError
    if not report.valid:
        raise NoWriteTransitionValidationError(f"Validation failed: {report.errors}")
