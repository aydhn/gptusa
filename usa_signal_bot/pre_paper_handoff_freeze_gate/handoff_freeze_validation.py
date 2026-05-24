import json
from dataclasses import dataclass, field
from typing import Any, List, Optional
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    FinalPrePaperHandoffFreezeGate,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle,
    PrePaperHandoffFreezeFullReview
)

@dataclass
class HandoffFreezeValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class HandoffFreezeValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[HandoffFreezeValidationIssue]
    warnings: List[str]
    errors: List[str]

def _create_report(issues: List[HandoffFreezeValidationIssue]) -> HandoffFreezeValidationReport:
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    return HandoffFreezeValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "BLOCKED"]),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_final_handoff_freeze_gate_report(item: FinalPrePaperHandoffFreezeGate) -> HandoffFreezeValidationReport:
    issues = []
    if not item.activation_denied: issues.append(HandoffFreezeValidationIssue("ERROR", "activation_denied", "Must be true"))
    if item.activation_allowed: issues.append(HandoffFreezeValidationIssue("ERROR", "activation_allowed", "Must be false"))
    if item.admission_allowed: issues.append(HandoffFreezeValidationIssue("ERROR", "admission_allowed", "Must be false"))
    if item.transition_allowed: issues.append(HandoffFreezeValidationIssue("ERROR", "transition_allowed", "Must be false"))
    if item.sandbox_runtime_admission_allowed: issues.append(HandoffFreezeValidationIssue("ERROR", "sandbox_runtime_admission_allowed", "Must be false"))
    if item.paper_sandbox_runtime_allowed: issues.append(HandoffFreezeValidationIssue("ERROR", "paper_sandbox_runtime_allowed", "Must be false"))
    if item.simulator_admission_allowed: issues.append(HandoffFreezeValidationIssue("ERROR", "simulator_admission_allowed", "Must be false"))
    if item.local_paper_simulator_allowed: issues.append(HandoffFreezeValidationIssue("ERROR", "local_paper_simulator_allowed", "Must be false"))
    if item.active_paper_enabled: issues.append(HandoffFreezeValidationIssue("ERROR", "active_paper_enabled", "Must be false"))
    if not item.pre_paper_handoff_complete: issues.append(HandoffFreezeValidationIssue("WARNING", "pre_paper_handoff_complete", "Should be true"))
    if not item.handoff_is_metadata_only: issues.append(HandoffFreezeValidationIssue("ERROR", "handoff_is_metadata_only", "Must be true"))
    if not item.all_writes_blocked: issues.append(HandoffFreezeValidationIssue("ERROR", "all_writes_blocked", "Must be true"))
    if item.order_created: issues.append(HandoffFreezeValidationIssue("ERROR", "order_created", "Must be false"))
    if item.mutation_detected: issues.append(HandoffFreezeValidationIssue("ERROR", "mutation_detected", "Must be false"))
    if item.allows_active_paper: issues.append(HandoffFreezeValidationIssue("ERROR", "allows_active_paper", "Must be false"))
    if item.allows_broker_execution: issues.append(HandoffFreezeValidationIssue("ERROR", "allows_broker_execution", "Must be false"))
    if item.allows_paper_state_mutation: issues.append(HandoffFreezeValidationIssue("ERROR", "allows_paper_state_mutation", "Must be false"))
    if item.allows_config_patch: issues.append(HandoffFreezeValidationIssue("ERROR", "allows_config_patch", "Must be false"))
    if item.allows_telegram_real_send: issues.append(HandoffFreezeValidationIssue("ERROR", "allows_telegram_real_send", "Must be false"))
    return _create_report(issues)

def validate_sandbox_runtime_admission_replay_result_report(item: SandboxRuntimeAdmissionReplayResult) -> HandoffFreezeValidationReport:
    issues = []
    if item.allowed_attempt_count > 0:
        issues.append(HandoffFreezeValidationIssue("ERROR", "allowed_attempt_count", "Allowed attempts must be 0"))
    return _create_report(issues)

def validate_simulator_evidence_freeze_report(item: SimulatorEvidenceFreezeBundle) -> HandoffFreezeValidationReport:
    issues = []
    if item.missing_evidence_count > 0:
        issues.append(HandoffFreezeValidationIssue("ERROR", "missing_evidence_count", "Cannot have missing evidence"))
    if item.stale_evidence_count > 0:
        issues.append(HandoffFreezeValidationIssue("ERROR", "stale_evidence_count", "Cannot have stale evidence"))
    return _create_report(issues)

def validate_handoff_freeze_full_review_report(item: PrePaperHandoffFreezeFullReview) -> HandoffFreezeValidationReport:
    issues = []
    for g in item.gates:
        res = validate_final_handoff_freeze_gate_report(g)
        issues.extend(res.issues)
    for r in item.sandbox_replay_results:
        res = validate_sandbox_runtime_admission_replay_result_report(r)
        issues.extend(res.issues)
    for e in item.evidence_freezes:
        res = validate_simulator_evidence_freeze_report(e)
        issues.extend(res.issues)
    return _create_report(issues)

def _validate_no_fields(payload: dict[str, Any], fields: List[str], label: str) -> HandoffFreezeValidationReport:
    issues = []
    payload_str = json.dumps(payload)
    for f in fields:
        if f in payload_str:
            issues.append(HandoffFreezeValidationIssue("ERROR", f, f"{label} field {f} detected"))
    return _create_report(issues)

def validate_no_sensitive_data_in_handoff_freeze_payload(payload: dict[str, Any]) -> HandoffFreezeValidationReport:
    return _validate_no_fields(payload, ["token", "secret", "api_key", "password"], "Sensitive data")

def validate_no_live_execution_language_in_handoff_freeze(text: str) -> HandoffFreezeValidationReport:
    issues = []
    text_lower = text.lower()
    phrases = ["live approved", "sent to broker", "kesin al", "garanti"]
    for p in phrases:
        if p in text_lower:
            issues.append(HandoffFreezeValidationIssue("ERROR", p, f"Live execution language detected: {p}"))
    return _create_report(issues)

def validate_no_active_paper_language_in_handoff_freeze(text: str) -> HandoffFreezeValidationReport:
    issues = []
    text_lower = text.lower()
    phrases = ["paper'a uygula", "canliya al", "gercek emir", "aktif et", "sandbox runtime baslat", "sandbox admission ac", "paper sandbox ac", "phase 101 aktif trading ac", "kesin kar", "candidate kesin iyi"]
    # also normalized ascii if necessary, keeping simple matching here
    for p in phrases:
        if p in text_lower:
            issues.append(HandoffFreezeValidationIssue("ERROR", p, f"Active paper language detected: {p}"))
    return _create_report(issues)

def validate_no_sandbox_runtime_admission_language(text: str) -> HandoffFreezeValidationReport:
    issues = []
    text_lower = text.lower()
    phrases = ["sandbox runtime baslat", "sandbox admission ac"]
    for p in phrases:
        if p in text_lower:
            issues.append(HandoffFreezeValidationIssue("ERROR", p, f"Sandbox admission language detected: {p}"))
    return _create_report(issues)

def validate_no_paper_state_mutation_fields_in_handoff_freeze(payload: dict[str, Any]) -> HandoffFreezeValidationReport:
    fields = ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]
    return _validate_no_fields(payload, fields, "Paper mutation")

def validate_no_broker_execution_fields_in_handoff_freeze(payload: dict[str, Any]) -> HandoffFreezeValidationReport:
    fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    return _validate_no_fields(payload, fields, "Broker execution")

def handoff_freeze_validation_report_to_text(report: HandoffFreezeValidationReport) -> str:
    res = f"Validation Report:\nValid: {report.valid}\nIssues: {report.issue_count} (Errors: {report.error_count}, Warnings: {report.warning_count}, Blocked: {report.blocked_count})\n"
    for i in report.issues:
        res += f"- [{i.severity}] {i.field}: {i.message}\n"
    return res

def assert_handoff_freeze_valid(report: HandoffFreezeValidationReport) -> None:
    if not report.valid:
        raise ValueError(f"Handoff freeze validation failed: {report.errors}")
