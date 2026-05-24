import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from usa_signal_bot.core.enums import (
    LocalPaperAdmissionSimulatorDossierStatus,
    LocalPaperAdmissionSimulatorDossierDecision,
    SimulatorDossierEvidenceStatus,
    SimulatorAcceptanceSealStatus,
    SimulatorAcceptanceSealDecision,
    PaperSandboxRuntimeAdmissionBlockerStatus,
    PaperSandboxRuntimeAdmissionBlockerDecision,
    PaperSandboxRuntimeAdmissionAttemptType,
    PaperSandboxRuntimeAdmissionBlockerAction,
    SimulatorDossierRiskFlag,
    SimulatorDossierReportType,
)

@dataclass
class SimulatorDossierEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    status: SimulatorDossierEvidenceStatus
    required: bool
    available: bool
    fresh: bool
    stale: bool
    summary: dict[str, Any]
    risk_flags: list[SimulatorDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    source_ref_id: Optional[str] = None
    source_path: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorAcceptanceSeal:
    seal_id: str
    created_at_utc: str
    status: SimulatorAcceptanceSealStatus
    decision: SimulatorAcceptanceSealDecision
    accepted_boundaries: list[str]
    simulator_gate_passed: bool
    rehearsal_replay_passed: bool
    dry_admission_evidence_freeze_valid: bool
    simulator_rules_passed: bool
    simulator_assertions_passed: bool
    no_simulator_admission_confirmed: bool
    no_local_paper_simulator_confirmed: bool
    no_sandbox_runtime_admission_confirmed: bool
    no_paper_sandbox_runtime_confirmed: bool
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
    allows_simulator_admission: bool
    allows_local_paper_simulator: bool
    allows_sandbox_runtime_admission: bool
    allows_paper_sandbox_runtime: bool
    allows_rehearsal: bool
    allows_paper_mode_rehearsal: bool
    allows_shadow_launch: bool
    allows_paper_mode_launch: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    risk_flags: list[SimulatorDossierRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    candidate_id: Optional[str] = None
    source_simulator_gate_id: Optional[str] = None
    source_simulator_review_id: Optional[str] = None
    source_rehearsal_replay_result_id: Optional[str] = None
    source_dry_admission_evidence_freeze_id: Optional[str] = None
    seal_hash: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSandboxRuntimeAdmissionBlockerRule:
    rule_id: str
    created_at_utc: str
    attempt_type: PaperSandboxRuntimeAdmissionAttemptType
    enabled: bool
    blocking: bool
    action: PaperSandboxRuntimeAdmissionBlockerAction
    description: str
    risk_flags: list[SimulatorDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSandboxRuntimeAdmissionBlockerEvent:
    event_id: str
    created_at_utc: str
    attempt_type: PaperSandboxRuntimeAdmissionAttemptType
    status: PaperSandboxRuntimeAdmissionBlockerStatus
    decision: PaperSandboxRuntimeAdmissionBlockerDecision
    action: PaperSandboxRuntimeAdmissionBlockerAction
    blocked: bool
    sandbox_runtime_admission_allowed: bool
    paper_sandbox_runtime_allowed: bool
    simulator_admission_allowed: bool
    local_paper_simulator_allowed: bool
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
    payload_summary: dict[str, Any]
    risk_flags: list[SimulatorDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    source_component: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class LocalPaperAdmissionSimulatorGateDossier:
    dossier_id: str
    created_at_utc: str
    status: LocalPaperAdmissionSimulatorDossierStatus
    decision: LocalPaperAdmissionSimulatorDossierDecision
    evidence_items: list[SimulatorDossierEvidenceItem]
    sandbox_runtime_admission_blocker_events: list[PaperSandboxRuntimeAdmissionBlockerEvent]
    evidence_refs: list[str]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    simulator_admission_allowed: bool
    local_paper_simulator_allowed: bool
    sandbox_runtime_admission_allowed: bool
    paper_sandbox_runtime_allowed: bool
    rehearsal_allowed: bool
    paper_mode_rehearsal_allowed: bool
    shadow_launch_allowed: bool
    paper_mode_launch_allowed: bool
    simulator_gate_passed: bool
    dry_admission_dossier_valid: bool
    acceptance_seal_valid: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: list[SimulatorDossierRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    acceptance_seal: Optional[SimulatorAcceptanceSeal] = None
    candidate_id: Optional[str] = None
    source_simulator_review_id: Optional[str] = None
    source_simulator_gate_id: Optional[str] = None
    source_rehearsal_replay_result_id: Optional[str] = None
    source_dry_admission_evidence_freeze_id: Optional[str] = None
    dossier_hash: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorDossierAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[SimulatorDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    decision: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorDossierFullReview:
    review_id: str
    created_at_utc: str
    report_type: SimulatorDossierReportType
    dossiers: list[LocalPaperAdmissionSimulatorGateDossier]
    evidence_items: list[SimulatorDossierEvidenceItem]
    acceptance_seals: list[SimulatorAcceptanceSeal]
    sandbox_runtime_admission_blocker_rules: list[PaperSandboxRuntimeAdmissionBlockerRule]
    sandbox_runtime_admission_blocker_events: list[PaperSandboxRuntimeAdmissionBlockerEvent]
    audit_entries: list[SimulatorDossierAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]


def create_simulator_dossier_evidence_id(prefix: str = "simulator_dossier_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_acceptance_seal_id(prefix: str = "simulator_acceptance_seal") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_runtime_admission_blocker_rule_id(prefix: str = "sandbox_runtime_admission_blocker_rule") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_runtime_admission_blocker_event_id(prefix: str = "sandbox_runtime_admission_blocker_event") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_dossier_id(prefix: str = "local_paper_admission_simulator_dossier") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_dossier_audit_id(prefix: str = "simulator_dossier_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_simulator_dossier_full_review_id(prefix: str = "simulator_dossier_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def simulator_dossier_evidence_item_to_dict(item: SimulatorDossierEvidenceItem) -> dict[str, Any]:
    return {
        "evidence_id": item.evidence_id,
        "created_at_utc": item.created_at_utc,
        "evidence_type": item.evidence_type,
        "status": item.status.value,
        "required": item.required,
        "available": item.available,
        "fresh": item.fresh,
        "stale": item.stale,
        "summary": item.summary,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "source_ref_id": item.source_ref_id,
        "source_path": item.source_path,
        "metadata": item.metadata,
    }

def simulator_acceptance_seal_to_dict(item: SimulatorAcceptanceSeal) -> dict[str, Any]:
    return {
        "seal_id": item.seal_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "accepted_boundaries": item.accepted_boundaries,
        "simulator_gate_passed": item.simulator_gate_passed,
        "rehearsal_replay_passed": item.rehearsal_replay_passed,
        "dry_admission_evidence_freeze_valid": item.dry_admission_evidence_freeze_valid,
        "simulator_rules_passed": item.simulator_rules_passed,
        "simulator_assertions_passed": item.simulator_assertions_passed,
        "no_simulator_admission_confirmed": item.no_simulator_admission_confirmed,
        "no_local_paper_simulator_confirmed": item.no_local_paper_simulator_confirmed,
        "no_sandbox_runtime_admission_confirmed": item.no_sandbox_runtime_admission_confirmed,
        "no_paper_sandbox_runtime_confirmed": item.no_paper_sandbox_runtime_confirmed,
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
        "allows_simulator_admission": item.allows_simulator_admission,
        "allows_local_paper_simulator": item.allows_local_paper_simulator,
        "allows_sandbox_runtime_admission": item.allows_sandbox_runtime_admission,
        "allows_paper_sandbox_runtime": item.allows_paper_sandbox_runtime,
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
        "candidate_id": item.candidate_id,
        "source_simulator_gate_id": item.source_simulator_gate_id,
        "source_simulator_review_id": item.source_simulator_review_id,
        "source_rehearsal_replay_result_id": item.source_rehearsal_replay_result_id,
        "source_dry_admission_evidence_freeze_id": item.source_dry_admission_evidence_freeze_id,
        "seal_hash": item.seal_hash,
        "metadata": item.metadata,
    }

def sandbox_runtime_admission_blocker_rule_to_dict(item: PaperSandboxRuntimeAdmissionBlockerRule) -> dict[str, Any]:
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

def sandbox_runtime_admission_blocker_event_to_dict(item: PaperSandboxRuntimeAdmissionBlockerEvent) -> dict[str, Any]:
    return {
        "event_id": item.event_id,
        "created_at_utc": item.created_at_utc,
        "attempt_type": item.attempt_type.value,
        "status": item.status.value,
        "decision": item.decision.value,
        "action": item.action.value,
        "blocked": item.blocked,
        "sandbox_runtime_admission_allowed": item.sandbox_runtime_admission_allowed,
        "paper_sandbox_runtime_allowed": item.paper_sandbox_runtime_allowed,
        "simulator_admission_allowed": item.simulator_admission_allowed,
        "local_paper_simulator_allowed": item.local_paper_simulator_allowed,
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
        "payload_summary": item.payload_summary,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "source_component": item.source_component,
        "metadata": item.metadata,
    }

def local_paper_admission_simulator_gate_dossier_to_dict(item: LocalPaperAdmissionSimulatorGateDossier) -> dict[str, Any]:
    return {
        "dossier_id": item.dossier_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value,
        "decision": item.decision.value,
        "evidence_items": [simulator_dossier_evidence_item_to_dict(e) for e in item.evidence_items],
        "acceptance_seal": simulator_acceptance_seal_to_dict(item.acceptance_seal) if item.acceptance_seal else None,
        "sandbox_runtime_admission_blocker_events": [sandbox_runtime_admission_blocker_event_to_dict(e) for e in item.sandbox_runtime_admission_blocker_events],
        "evidence_refs": item.evidence_refs,
        "sealed": item.sealed,
        "immutable": item.immutable,
        "manual_review_required": item.manual_review_required,
        "activation_denied": item.activation_denied,
        "activation_allowed": item.activation_allowed,
        "admission_allowed": item.admission_allowed,
        "transition_allowed": item.transition_allowed,
        "simulator_admission_allowed": item.simulator_admission_allowed,
        "local_paper_simulator_allowed": item.local_paper_simulator_allowed,
        "sandbox_runtime_admission_allowed": item.sandbox_runtime_admission_allowed,
        "paper_sandbox_runtime_allowed": item.paper_sandbox_runtime_allowed,
        "rehearsal_allowed": item.rehearsal_allowed,
        "paper_mode_rehearsal_allowed": item.paper_mode_rehearsal_allowed,
        "shadow_launch_allowed": item.shadow_launch_allowed,
        "paper_mode_launch_allowed": item.paper_mode_launch_allowed,
        "simulator_gate_passed": item.simulator_gate_passed,
        "dry_admission_dossier_valid": item.dry_admission_dossier_valid,
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
        "candidate_id": item.candidate_id,
        "source_simulator_review_id": item.source_simulator_review_id,
        "source_simulator_gate_id": item.source_simulator_gate_id,
        "source_rehearsal_replay_result_id": item.source_rehearsal_replay_result_id,
        "source_dry_admission_evidence_freeze_id": item.source_dry_admission_evidence_freeze_id,
        "dossier_hash": item.dossier_hash,
        "metadata": item.metadata,
    }

def simulator_dossier_audit_entry_to_dict(item: SimulatorDossierAuditEntry) -> dict[str, Any]:
    return {
        "audit_id": item.audit_id,
        "created_at_utc": item.created_at_utc,
        "entity_type": item.entity_type,
        "entity_id": item.entity_id,
        "action": item.action,
        "rationale": item.rationale,
        "evidence_refs": item.evidence_refs,
        "risk_flags": [f.value for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "decision": item.decision,
        "metadata": item.metadata,
    }

def simulator_dossier_full_review_to_dict(item: SimulatorDossierFullReview) -> dict[str, Any]:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "dossiers": [local_paper_admission_simulator_gate_dossier_to_dict(d) for d in item.dossiers],
        "evidence_items": [simulator_dossier_evidence_item_to_dict(e) for e in item.evidence_items],
        "acceptance_seals": [simulator_acceptance_seal_to_dict(s) for s in item.acceptance_seals],
        "sandbox_runtime_admission_blocker_rules": [sandbox_runtime_admission_blocker_rule_to_dict(r) for r in item.sandbox_runtime_admission_blocker_rules],
        "sandbox_runtime_admission_blocker_events": [sandbox_runtime_admission_blocker_event_to_dict(e) for e in item.sandbox_runtime_admission_blocker_events],
        "audit_entries": [simulator_dossier_audit_entry_to_dict(a) for a in item.audit_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }
