from pathlib import Path

p = Path("usa_signal_bot/paper_mode_dry_admission_gate/dry_admission_validation.py")
content = p.read_text()
# We already imported `field` correctly, but perhaps the import was duplicated or shadowed. Let's rewrite the imports properly.

new_content = """from dataclasses import dataclass, field
from typing import Any, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    FinalPaperModeDryAdmissionGate,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle,
    DryAdmissionGateFullReview
)

@dataclass
class DryAdmissionValidationIssue:
    severity: str
    message: str
    field: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[DryAdmissionValidationIssue]
    warnings: List[str]
    errors: List[str]


def _create_report(issues: List[DryAdmissionValidationIssue]) -> DryAdmissionValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity == "ERROR"]
    blocks = [i.message for i in issues if i.severity == "BLOCK"]

    return DryAdmissionValidationReport(
        valid=len(errors) == 0 and len(blocks) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len(blocks),
        issues=issues,
        warnings=warnings,
        errors=errors + blocks
    )

def validate_final_dry_admission_gate_report(item: FinalPaperModeDryAdmissionGate) -> DryAdmissionValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(DryAdmissionValidationIssue("ERROR", "activation_denied must be True"))
    if item.activation_allowed:
        issues.append(DryAdmissionValidationIssue("ERROR", "activation_allowed must be False"))
    if item.admission_allowed:
        issues.append(DryAdmissionValidationIssue("ERROR", "admission_allowed must be False"))
    if item.transition_allowed:
        issues.append(DryAdmissionValidationIssue("ERROR", "transition_allowed must be False"))
    if item.shadow_launch_allowed:
        issues.append(DryAdmissionValidationIssue("ERROR", "shadow_launch_allowed must be False"))
    if item.paper_mode_launch_allowed:
        issues.append(DryAdmissionValidationIssue("ERROR", "paper_mode_launch_allowed must be False"))
    if not item.all_writes_blocked:
        issues.append(DryAdmissionValidationIssue("ERROR", "all_writes_blocked must be True"))
    if item.order_created:
        issues.append(DryAdmissionValidationIssue("ERROR", "order_created must be False"))
    if item.mutation_detected:
        issues.append(DryAdmissionValidationIssue("ERROR", "mutation_detected must be False"))
    if item.allows_active_paper:
        issues.append(DryAdmissionValidationIssue("ERROR", "allows_active_paper must be False"))
    if item.allows_broker_execution:
        issues.append(DryAdmissionValidationIssue("ERROR", "allows_broker_execution must be False"))
    if item.allows_paper_state_mutation:
        issues.append(DryAdmissionValidationIssue("ERROR", "allows_paper_state_mutation must be False"))
    if item.allows_config_patch:
        issues.append(DryAdmissionValidationIssue("ERROR", "allows_config_patch must be False"))
    if item.allows_telegram_real_send:
        issues.append(DryAdmissionValidationIssue("ERROR", "allows_telegram_real_send must be False"))
    if not item.dry_admission_gate_passed:
        issues.append(DryAdmissionValidationIssue("BLOCK", "dry_admission_gate_passed is False"))
    return _create_report(issues)

def validate_shadow_replay_result_report(item: ShadowLaunchReplayResult) -> DryAdmissionValidationReport:
    issues = []
    if item.allowed_attempt_count > 0:
        issues.append(DryAdmissionValidationIssue("ERROR", "allowed_attempt_count must be 0"))
    return _create_report(issues)

def validate_board_evidence_freeze_report(item: BoardEvidenceFreezeBundle) -> DryAdmissionValidationReport:
    issues = []
    if item.missing_evidence_count > 0:
        issues.append(DryAdmissionValidationIssue("ERROR", "Missing evidence"))
    if item.stale_evidence_count > 0:
        issues.append(DryAdmissionValidationIssue("ERROR", "Stale evidence"))
    return _create_report(issues)

def validate_dry_admission_full_review_report(item: DryAdmissionGateFullReview) -> DryAdmissionValidationReport:
    issues = []
    for g in item.gates:
        rep = validate_final_dry_admission_gate_report(g)
        issues.extend(rep.issues)
    for sr in item.shadow_replay_results:
        rep = validate_shadow_replay_result_report(sr)
        issues.extend(rep.issues)
    for f in item.evidence_freezes:
        rep = validate_board_evidence_freeze_report(f)
        issues.extend(rep.issues)
    return _create_report(issues)

def validate_no_sensitive_data_in_dry_admission_payload(payload: dict[str, Any]) -> DryAdmissionValidationReport:
    issues = []
    str_payload = str(payload).lower()
    for secret in ["api_key", "secret", "password", "token"]:
        if secret in str_payload:
            issues.append(DryAdmissionValidationIssue("ERROR", f"Potential sensitive data: {secret}"))
    return _create_report(issues)

def validate_no_live_execution_language_in_dry_admission(text: str) -> DryAdmissionValidationReport:
    issues = []
    text = text.lower()
    for forbidden in ["live approved", "sent to broker", "kesin al", "garanti", "gerçek emir"]:
        if forbidden in text:
            issues.append(DryAdmissionValidationIssue("BLOCK", f"Forbidden live language: {forbidden}"))
    return _create_report(issues)

def validate_no_active_paper_language_in_dry_admission(text: str) -> DryAdmissionValidationReport:
    issues = []
    text = text.lower()
    for forbidden in ["paper'a uygula", "canlıya al", "aktif et", "kesin kâr"]:
        if forbidden in text:
            issues.append(DryAdmissionValidationIssue("BLOCK", f"Forbidden active paper language: {forbidden}"))
    return _create_report(issues)

def validate_no_shadow_launch_language_in_dry_admission(text: str) -> DryAdmissionValidationReport:
    issues = []
    text = text.lower()
    for forbidden in ["shadow launch başlat", "paper mode başlat"]:
        if forbidden in text:
            issues.append(DryAdmissionValidationIssue("BLOCK", f"Forbidden shadow launch language: {forbidden}"))
    return _create_report(issues)

def validate_no_paper_state_mutation_fields_in_dry_admission(payload: dict[str, Any]) -> DryAdmissionValidationReport:
    issues = []
    str_payload = str(payload)
    for field in ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]:
        if f"'{field}': True" in str_payload or f'"{field}": true' in str_payload.lower():
             issues.append(DryAdmissionValidationIssue("BLOCK", f"Forbidden paper mutation field active: {field}"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_dry_admission(payload: dict[str, Any]) -> DryAdmissionValidationReport:
    issues = []
    str_payload = str(payload)
    for field in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if field in str_payload:
            issues.append(DryAdmissionValidationIssue("BLOCK", f"Forbidden broker execution field: {field}"))
    return _create_report(issues)

def dry_admission_validation_report_to_text(report: DryAdmissionValidationReport) -> str:
    return f"Validation Report - Valid: {report.valid}, Errors: {report.error_count}, Blocked: {report.blocked_count}"

def assert_dry_admission_valid(report: DryAdmissionValidationReport) -> None:
    from usa_signal_bot.core.exceptions import DryAdmissionValidationError
    if not report.valid:
        raise DryAdmissionValidationError(f"Validation failed: {report.errors}")
"""

p.write_text(new_content)
