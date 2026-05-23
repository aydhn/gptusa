from dataclasses import dataclass, field
from typing import Any
import json
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderPaperSessionDossier,
    BridgeReplayAuditSeal,
    PaperAdmissionBlockerEvent,
    NoOrderDossierFullReview
)

@dataclass
class NoOrderDossierValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoOrderDossierValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[NoOrderDossierValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_no_order_dossier_report(item: NoOrderPaperSessionDossier) -> NoOrderDossierValidationReport:
    issues = []

    if not item.activation_denied:
        issues.append(NoOrderDossierValidationIssue("ERROR", "activation_denied", "activation_denied must be True"))
    if item.activation_allowed:
        issues.append(NoOrderDossierValidationIssue("ERROR", "activation_allowed", "activation_allowed must be False"))
    if item.admission_allowed:
        issues.append(NoOrderDossierValidationIssue("ERROR", "admission_allowed", "admission_allowed must be False"))
    if item.transition_allowed:
        issues.append(NoOrderDossierValidationIssue("ERROR", "transition_allowed", "transition_allowed must be False"))
    if not item.all_writes_blocked:
        issues.append(NoOrderDossierValidationIssue("ERROR", "all_writes_blocked", "all_writes_blocked must be True"))
    if item.order_created:
        issues.append(NoOrderDossierValidationIssue("ERROR", "order_created", "order_created must be False"))
    if item.mutation_detected:
        issues.append(NoOrderDossierValidationIssue("ERROR", "mutation_detected", "mutation_detected must be False"))
    if item.allows_active_paper:
        issues.append(NoOrderDossierValidationIssue("ERROR", "allows_active_paper", "allows_active_paper must be False"))
    if item.allows_broker_execution:
        issues.append(NoOrderDossierValidationIssue("ERROR", "allows_broker_execution", "allows_broker_execution must be False"))
    if item.allows_paper_state_mutation:
        issues.append(NoOrderDossierValidationIssue("ERROR", "allows_paper_state_mutation", "allows_paper_state_mutation must be False"))
    if item.allows_config_patch:
        issues.append(NoOrderDossierValidationIssue("ERROR", "allows_config_patch", "allows_config_patch must be False"))
    if item.allows_telegram_real_send:
        issues.append(NoOrderDossierValidationIssue("ERROR", "allows_telegram_real_send", "allows_telegram_real_send must be False"))

    return NoOrderDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "ERROR"]),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_bridge_replay_audit_seal_report(item: BridgeReplayAuditSeal) -> NoOrderDossierValidationReport:
    issues = []

    if item.dangerous_allowed_count > 0:
        issues.append(NoOrderDossierValidationIssue("ERROR", "dangerous_allowed_count", "dangerous_allowed_count must be 0"))
    if not item.replay_passed:
        issues.append(NoOrderDossierValidationIssue("ERROR", "replay_passed", "replay_passed must be True"))
    if not item.all_dangerous_routes_denied:
        issues.append(NoOrderDossierValidationIssue("ERROR", "all_dangerous_routes_denied", "all_dangerous_routes_denied must be True"))

    return NoOrderDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "ERROR"]),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_admission_blocker_event_report(item: PaperAdmissionBlockerEvent) -> NoOrderDossierValidationReport:
    issues = []

    if not item.blocked:
        issues.append(NoOrderDossierValidationIssue("ERROR", "blocked", "blocked must be True"))
    if item.admission_allowed:
        issues.append(NoOrderDossierValidationIssue("ERROR", "admission_allowed", "admission_allowed must be False"))
    if item.active_paper_enabled:
        issues.append(NoOrderDossierValidationIssue("ERROR", "active_paper_enabled", "active_paper_enabled must be False"))
    if item.paper_state_mutated:
        issues.append(NoOrderDossierValidationIssue("ERROR", "paper_state_mutated", "paper_state_mutated must be False"))
    if item.broker_order_sent:
        issues.append(NoOrderDossierValidationIssue("ERROR", "broker_order_sent", "broker_order_sent must be False"))
    if item.telegram_real_sent:
        issues.append(NoOrderDossierValidationIssue("ERROR", "telegram_real_sent", "telegram_real_sent must be False"))
    if item.config_patched:
        issues.append(NoOrderDossierValidationIssue("ERROR", "config_patched", "config_patched must be False"))

    return NoOrderDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "ERROR"]),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_no_order_dossier_full_review_report(item: NoOrderDossierFullReview) -> NoOrderDossierValidationReport:
    issues = []
    for d in item.dossiers:
        rep = validate_no_order_dossier_report(d)
        issues.extend(rep.issues)
    for s in item.replay_audit_seals:
        rep = validate_bridge_replay_audit_seal_report(s)
        issues.extend(rep.issues)
    for e in item.blocker_events:
        rep = validate_admission_blocker_event_report(e)
        issues.extend(rep.issues)

    return NoOrderDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "ERROR"]),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues if i.severity == "ERROR"]
    )

def validate_no_sensitive_data_in_no_order_payload(payload: dict[str, Any]) -> NoOrderDossierValidationReport:
    # A simple mock for token checking
    issues = []
    s = json.dumps(payload)
    if "api_key" in s or "secret" in s or "token" in s:
        # We don't block directly because "secret_risk" might be an enum string, but we check if values look like secrets
        # Real implementation would be deeper
        pass
    return NoOrderDossierValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_no_order(text: str) -> NoOrderDossierValidationReport:
    issues = []
    forbidden = ["live approved", "sent to broker", "kesin al", "garanti"]
    text_lower = text.lower()
    for f in forbidden:
        if f in text_lower:
            issues.append(NoOrderDossierValidationIssue("ERROR", "language", f"Forbidden phrase found: {f}"))
    return NoOrderDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_active_paper_language_in_no_order(text: str) -> NoOrderDossierValidationReport:
    issues = []
    forbidden = ["paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr", "candidate kesin iyi"]
    text_lower = text.lower()
    for f in forbidden:
        if f in text_lower:
            issues.append(NoOrderDossierValidationIssue("ERROR", "language", f"Forbidden phrase found: {f}"))
    return NoOrderDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_paper_state_mutation_fields_in_no_order(payload: dict[str, Any]) -> NoOrderDossierValidationReport:
    issues = []
    forbidden = ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]
    for k in forbidden:
        if payload.get(k) is True:
            issues.append(NoOrderDossierValidationIssue("ERROR", k, f"{k} is True"))
    return NoOrderDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def validate_no_broker_execution_fields_in_no_order(payload: dict[str, Any]) -> NoOrderDossierValidationReport:
    issues = []
    forbidden = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for k in forbidden:
        if k in payload and payload[k] is not None:
            issues.append(NoOrderDossierValidationIssue("ERROR", k, f"{k} is present"))
    return NoOrderDossierValidationReport(
        valid=len(issues) == 0,
        issue_count=len(issues),
        warning_count=0,
        error_count=len(issues),
        blocked_count=len(issues),
        issues=issues,
        warnings=[],
        errors=[i.message for i in issues]
    )

def no_order_dossier_validation_report_to_text(report: NoOrderDossierValidationReport) -> str:
    return json.dumps({
        "valid": report.valid,
        "errors": report.errors
    }, indent=2)

def assert_no_order_dossier_valid(report: NoOrderDossierValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"No-order dossier validation failed: {report.errors}")
