import os

path = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier_models.py"

content = """from dataclasses import dataclass, field
from typing import Any
import uuid
import datetime

from usa_signal_bot.core.enums import (
    DryAdmissionDossierStatus,
    DryAdmissionDossierDecision,
    DryAdmissionDossierEvidenceStatus,
    DryAdmissionAcceptanceSealStatus,
    DryAdmissionAcceptanceSealDecision,
    PaperModeRehearsalBlockerStatus,
    PaperModeRehearsalBlockerDecision,
    PaperModeRehearsalAttemptType,
    PaperModeRehearsalBlockerAction,
    DryAdmissionDossierRiskFlag,
    DryAdmissionDossierReportType
)

@dataclass
class DryAdmissionDossierEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    source_ref_id: str | None
    source_path: str | None
    status: DryAdmissionDossierEvidenceStatus
    required: bool
    available: bool
    fresh: bool
    stale: bool
    summary: dict[str, Any]
    risk_flags: list[DryAdmissionDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionAcceptanceSeal:
    seal_id: str
    created_at_utc: str
    status: DryAdmissionAcceptanceSealStatus
    decision: DryAdmissionAcceptanceSealDecision
    candidate_id: str | None
    source_dry_admission_gate_id: str | None
    source_dry_admission_review_id: str | None
    source_shadow_replay_result_id: str | None
    source_board_evidence_freeze_id: str | None
    seal_hash: str | None
    accepted_boundaries: list[str]
    dry_admission_gate_passed: bool
    shadow_replay_passed: bool
    board_evidence_freeze_valid: bool
    dry_admission_rules_passed: bool
    dry_admission_assertions_passed: bool
    no_shadow_launch_confirmed: bool
    no_paper_mode_launch_confirmed: bool
    no_rehearsal_confirmed: bool
    no_admission_confirmed: bool
    no_order_confirmed: bool
    no_write_confirmed: bool
    no_broker_confirmed: bool
    no_config_patch_confirmed: bool
    no_telegram_real_send_confirmed: bool
    sealed: bool
    immutable: bool
    seal_is_metadata_only: bool
    allows_rehearsal: bool
    allows_paper_mode_rehearsal: bool
    allows_shadow_launch: bool
    allows_paper_mode_launch: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    risk_flags: list[DryAdmissionDossierRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperModeRehearsalBlockerRule:
    rule_id: str
    created_at_utc: str
    attempt_type: PaperModeRehearsalAttemptType
    enabled: bool
    blocking: bool
    action: PaperModeRehearsalBlockerAction
    description: str
    risk_flags: list[DryAdmissionDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperModeRehearsalBlockerEvent:
    event_id: str
    created_at_utc: str
    attempt_type: PaperModeRehearsalAttemptType
    status: PaperModeRehearsalBlockerStatus
    decision: PaperModeRehearsalBlockerDecision
    action: PaperModeRehearsalBlockerAction
    blocked: bool
    rehearsal_allowed: bool
    paper_mode_rehearsal_allowed: bool
    shadow_launch_allowed: bool
    paper_mode_launch_allowed: bool
    admission_allowed: bool
    active_paper_enabled: bool
    order_created: bool
    paper_state_mutated: bool
    broker_order_sent: bool
    telegram_real_sent: bool
    config_patched: bool
    source_component: str | None
    payload_summary: dict[str, Any]
    risk_flags: list[DryAdmissionDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionGateDossier:
    dossier_id: str
    created_at_utc: str
    status: DryAdmissionDossierStatus
    decision: DryAdmissionDossierDecision
    candidate_id: str | None
    source_dry_admission_review_id: str | None
    source_dry_admission_gate_id: str | None
    source_shadow_replay_result_id: str | None
    source_board_evidence_freeze_id: str | None
    evidence_items: list[DryAdmissionDossierEvidenceItem]
    acceptance_seal: DryAdmissionAcceptanceSeal | None
    rehearsal_blocker_events: list[PaperModeRehearsalBlockerEvent]
    evidence_refs: list[str]
    dossier_hash: str | None
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    shadow_launch_allowed: bool
    paper_mode_launch_allowed: bool
    rehearsal_allowed: bool
    paper_mode_rehearsal_allowed: bool
    dry_admission_gate_passed: bool
    board_dossier_valid: bool
    acceptance_seal_valid: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: list[DryAdmissionDossierRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionDossierAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: str | None
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[DryAdmissionDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionDossierFullReview:
    review_id: str
    created_at_utc: str
    report_type: DryAdmissionDossierReportType
    dossiers: list[DryAdmissionGateDossier]
    evidence_items: list[DryAdmissionDossierEvidenceItem]
    acceptance_seals: list[DryAdmissionAcceptanceSeal]
    rehearsal_blocker_rules: list[PaperModeRehearsalBlockerRule]
    rehearsal_blocker_events: list[PaperModeRehearsalBlockerEvent]
    audit_entries: list[DryAdmissionDossierAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def create_dry_admission_dossier_evidence_id(prefix: str = "dry_admission_dossier_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_acceptance_seal_id(prefix: str = "dry_admission_acceptance_seal") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_rehearsal_blocker_rule_id(prefix: str = "rehearsal_blocker_rule") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_rehearsal_blocker_event_id(prefix: str = "rehearsal_blocker_event") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_dossier_id(prefix: str = "dry_admission_dossier") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_dossier_audit_id(prefix: str = "dry_admission_dossier_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_dry_admission_dossier_full_review_id(prefix: str = "dry_admission_dossier_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def dry_admission_dossier_evidence_item_to_dict(item: DryAdmissionDossierEvidenceItem) -> dict:
    return {
        "evidence_id": item.evidence_id,
        "created_at_utc": item.created_at_utc,
        "evidence_type": item.evidence_type,
        "source_ref_id": item.source_ref_id,
        "source_path": item.source_path,
        "status": item.status.value,
        "required": item.required,
        "available": item.available,
        "fresh": item.fresh,
        "stale": item.stale,
        "summary": item.summary,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def dry_admission_acceptance_seal_to_dict(item: DryAdmissionAcceptanceSeal) -> dict:
    return {
        "seal_id": item.seal_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "source_dry_admission_gate_id": item.source_dry_admission_gate_id,
        "source_dry_admission_review_id": item.source_dry_admission_review_id,
        "source_shadow_replay_result_id": item.source_shadow_replay_result_id,
        "source_board_evidence_freeze_id": item.source_board_evidence_freeze_id,
        "seal_hash": item.seal_hash,
        "accepted_boundaries": item.accepted_boundaries,
        "dry_admission_gate_passed": item.dry_admission_gate_passed,
        "shadow_replay_passed": item.shadow_replay_passed,
        "board_evidence_freeze_valid": item.board_evidence_freeze_valid,
        "dry_admission_rules_passed": item.dry_admission_rules_passed,
        "dry_admission_assertions_passed": item.dry_admission_assertions_passed,
        "no_shadow_launch_confirmed": item.no_shadow_launch_confirmed,
        "no_paper_mode_launch_confirmed": item.no_paper_mode_launch_confirmed,
        "no_rehearsal_confirmed": item.no_rehearsal_confirmed,
        "no_admission_confirmed": item.no_admission_confirmed,
        "no_order_confirmed": item.no_order_confirmed,
        "no_write_confirmed": item.no_write_confirmed,
        "no_broker_confirmed": item.no_broker_confirmed,
        "no_config_patch_confirmed": item.no_config_patch_confirmed,
        "no_telegram_real_send_confirmed": item.no_telegram_real_send_confirmed,
        "sealed": item.sealed,
        "immutable": item.immutable,
        "seal_is_metadata_only": item.seal_is_metadata_only,
        "allows_rehearsal": item.allows_rehearsal,
        "allows_paper_mode_rehearsal": item.allows_paper_mode_rehearsal,
        "allows_shadow_launch": item.allows_shadow_launch,
        "allows_paper_mode_launch": item.allows_paper_mode_launch,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "risk_flags": [f.value for f in item.risk_flags],
        "required_followups": item.required_followups,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def rehearsal_blocker_rule_to_dict(item: PaperModeRehearsalBlockerRule) -> dict:
    return {
        "rule_id": item.rule_id,
        "created_at_utc": item.created_at_utc,
        "attempt_type": item.attempt_type.value,
        "enabled": item.enabled,
        "blocking": item.blocking,
        "action": item.action.value,
        "description": item.description,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def rehearsal_blocker_event_to_dict(item: PaperModeRehearsalBlockerEvent) -> dict:
    return {
        "event_id": item.event_id,
        "created_at_utc": item.created_at_utc,
        "attempt_type": item.attempt_type.value,
        "status": item.status.value,
        "decision": item.decision.value,
        "action": item.action.value,
        "blocked": item.blocked,
        "rehearsal_allowed": item.rehearsal_allowed,
        "paper_mode_rehearsal_allowed": item.paper_mode_rehearsal_allowed,
        "shadow_launch_allowed": item.shadow_launch_allowed,
        "paper_mode_launch_allowed": item.paper_mode_launch_allowed,
        "admission_allowed": item.admission_allowed,
        "active_paper_enabled": item.active_paper_enabled,
        "order_created": item.order_created,
        "paper_state_mutated": item.paper_state_mutated,
        "broker_order_sent": item.broker_order_sent,
        "telegram_real_sent": item.telegram_real_sent,
        "config_patched": item.config_patched,
        "source_component": item.source_component,
        "payload_summary": item.payload_summary,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def dry_admission_gate_dossier_to_dict(item: DryAdmissionGateDossier) -> dict:
    return {
        "dossier_id": item.dossier_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "candidate_id": item.candidate_id,
        "source_dry_admission_review_id": item.source_dry_admission_review_id,
        "source_dry_admission_gate_id": item.source_dry_admission_gate_id,
        "source_shadow_replay_result_id": item.source_shadow_replay_result_id,
        "source_board_evidence_freeze_id": item.source_board_evidence_freeze_id,
        "evidence_items": [dry_admission_dossier_evidence_item_to_dict(e) for e in item.evidence_items],
        "acceptance_seal": dry_admission_acceptance_seal_to_dict(item.acceptance_seal) if item.acceptance_seal else None,
        "rehearsal_blocker_events": [rehearsal_blocker_event_to_dict(e) for e in item.rehearsal_blocker_events],
        "evidence_refs": item.evidence_refs,
        "dossier_hash": item.dossier_hash,
        "sealed": item.sealed,
        "immutable": item.immutable,
        "manual_review_required": item.manual_review_required,
        "activation_denied": item.activation_denied,
        "activation_allowed": item.activation_allowed,
        "admission_allowed": item.admission_allowed,
        "transition_allowed": item.transition_allowed,
        "shadow_launch_allowed": item.shadow_launch_allowed,
        "paper_mode_launch_allowed": item.paper_mode_launch_allowed,
        "rehearsal_allowed": item.rehearsal_allowed,
        "paper_mode_rehearsal_allowed": item.paper_mode_rehearsal_allowed,
        "dry_admission_gate_passed": item.dry_admission_gate_passed,
        "board_dossier_valid": item.board_dossier_valid,
        "acceptance_seal_valid": item.acceptance_seal_valid,
        "all_writes_blocked": item.all_writes_blocked,
        "order_created": item.order_created,
        "mutation_detected": item.mutation_detected,
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "safety_flags": [f.value for f in item.safety_flags],
        "required_followups": item.required_followups,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def dry_admission_dossier_audit_entry_to_dict(item: DryAdmissionDossierAuditEntry) -> dict:
    return {
        "audit_id": item.audit_id,
        "created_at_utc": item.created_at_utc,
        "entity_type": item.entity_type,
        "entity_id": item.entity_id,
        "action": item.action,
        "decision": item.decision,
        "rationale": item.rationale,
        "evidence_refs": item.evidence_refs,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def dry_admission_dossier_full_review_to_dict(item: DryAdmissionDossierFullReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "dossiers": [dry_admission_gate_dossier_to_dict(d) for d in item.dossiers],
        "evidence_items": [dry_admission_dossier_evidence_item_to_dict(e) for e in item.evidence_items],
        "acceptance_seals": [dry_admission_acceptance_seal_to_dict(s) for s in item.acceptance_seals],
        "rehearsal_blocker_rules": [rehearsal_blocker_rule_to_dict(r) for r in item.rehearsal_blocker_rules],
        "rehearsal_blocker_events": [rehearsal_blocker_event_to_dict(e) for e in item.rehearsal_blocker_events],
        "audit_entries": [dry_admission_dossier_audit_entry_to_dict(a) for a in item.audit_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_dry_admission_dossier_evidence_item(item: DryAdmissionDossierEvidenceItem) -> None:
    pass

def validate_dry_admission_acceptance_seal(item: DryAdmissionAcceptanceSeal) -> None:
    if item.sealed and not item.immutable:
        item.errors.append("Sealed seal must be immutable")
    if not item.seal_is_metadata_only:
        item.errors.append("Seal must be metadata-only")
    if item.allows_rehearsal:
        item.errors.append("Seal cannot allow rehearsal")
    if item.allows_paper_mode_rehearsal:
        item.errors.append("Seal cannot allow paper mode rehearsal")
    if item.allows_active_paper:
        item.errors.append("Seal cannot allow active paper")
    if item.allows_broker_execution:
        item.errors.append("Seal cannot allow broker execution")
    if item.allows_paper_state_mutation:
        item.errors.append("Seal cannot allow paper state mutation")

def validate_rehearsal_blocker_rule(item: PaperModeRehearsalBlockerRule) -> None:
    if not item.enabled:
        item.errors.append("Rehearsal blocker rule must be enabled")
    if not item.blocking:
        item.errors.append("Rehearsal blocker rule must be blocking")

def validate_rehearsal_blocker_event(item: PaperModeRehearsalBlockerEvent) -> None:
    if not item.blocked:
        item.errors.append("Rehearsal blocker event must be blocked")
    if item.rehearsal_allowed:
        item.errors.append("Event cannot allow rehearsal")
    if item.paper_mode_rehearsal_allowed:
        item.errors.append("Event cannot allow paper mode rehearsal")
    if item.active_paper_enabled:
        item.errors.append("Event cannot enable active paper")
    if item.order_created:
        item.errors.append("Event cannot create order")
    if item.paper_state_mutated:
        item.errors.append("Event cannot mutate paper state")
    if item.broker_order_sent:
        item.errors.append("Event cannot send broker order")
    if item.telegram_real_sent:
        item.errors.append("Event cannot send telegram real message")
    if item.config_patched:
        item.errors.append("Event cannot patch config")

def validate_dry_admission_gate_dossier(item: DryAdmissionGateDossier) -> None:
    if item.sealed and not item.immutable:
        item.errors.append("Sealed dossier must be immutable")
    if not item.manual_review_required:
        item.errors.append("Manual review required flag must be true")
    if not item.activation_denied:
        item.errors.append("Activation denied flag must be true")
    if item.activation_allowed:
        item.errors.append("Dossier cannot allow activation")
    if item.admission_allowed:
        item.errors.append("Dossier cannot allow admission")
    if item.transition_allowed:
        item.errors.append("Dossier cannot allow transition")
    if item.shadow_launch_allowed:
        item.errors.append("Dossier cannot allow shadow launch")
    if item.paper_mode_launch_allowed:
        item.errors.append("Dossier cannot allow paper mode launch")
    if item.rehearsal_allowed:
        item.errors.append("Dossier cannot allow rehearsal")
    if item.paper_mode_rehearsal_allowed:
        item.errors.append("Dossier cannot allow paper mode rehearsal")
    if not item.dry_admission_gate_passed:
        item.errors.append("Dry admission gate passed flag must be true")
    if not item.board_dossier_valid:
        item.errors.append("Board dossier valid flag must be true")
    if not item.acceptance_seal_valid:
        item.errors.append("Acceptance seal valid flag must be true")
    if not item.all_writes_blocked:
        item.errors.append("All writes blocked flag must be true")
    if item.order_created:
        item.errors.append("Dossier cannot create order")
    if item.mutation_detected:
        item.errors.append("Dossier cannot detect mutation")
    if item.allows_active_paper:
        item.errors.append("Dossier cannot allow active paper")
    if item.allows_broker_execution:
        item.errors.append("Dossier cannot allow broker execution")
    if item.allows_paper_state_mutation:
        item.errors.append("Dossier cannot allow paper state mutation")
    if item.allows_config_patch:
        item.errors.append("Dossier cannot allow config patch")
    if item.allows_telegram_real_send:
        item.errors.append("Dossier cannot allow telegram real send")

def validate_dry_admission_dossier_full_review(item: DryAdmissionDossierFullReview) -> None:
    pass

"""

with open(path, "w") as f:
    f.write(content)

print("dossier models created")
