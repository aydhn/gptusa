from dataclasses import dataclass, field
from typing import Any, Optional, List
from usa_signal_bot.core.enums import (
    NoOrderSessionDossierStatus,
    NoOrderSessionDossierDecision,
    NoOrderDossierEvidenceStatus,
    BridgeReplayAuditSealStatus,
    BridgeReplayAuditSealDecision,
    PaperAdmissionBlockerStatus,
    PaperAdmissionBlockerDecision,
    PaperAdmissionAttemptType,
    PaperAdmissionBlockerAction,
    NoOrderDossierRiskFlag,
    NoOrderDossierReportType,
)

@dataclass
class NoOrderDossierEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    source_ref_id: Optional[str]
    source_path: Optional[str]
    status: NoOrderDossierEvidenceStatus
    required: bool
    available: bool
    fresh: bool
    stale: bool
    summary: dict[str, Any]
    risk_flags: list[NoOrderDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BridgeReplayAuditSeal:
    seal_id: str
    created_at_utc: str
    status: BridgeReplayAuditSealStatus
    decision: BridgeReplayAuditSealDecision
    candidate_id: Optional[str]
    source_bridge_replay_result_id: Optional[str]
    source_bridge_review_id: Optional[str]
    replay_hash: Optional[str]
    route_attempt_hash: Optional[str]
    dangerous_route_coverage_hash: Optional[str]
    sealed: bool
    immutable: bool
    replay_passed: bool
    all_dangerous_routes_denied: bool
    dangerous_allowed_count: int
    read_only_allowed_count: int
    missing_route_count: int
    evidence_refs: list[str]
    risk_flags: list[NoOrderDossierRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperAdmissionBlockerRule:
    rule_id: str
    created_at_utc: str
    attempt_type: PaperAdmissionAttemptType
    enabled: bool
    blocking: bool
    action: PaperAdmissionBlockerAction
    description: str
    risk_flags: list[NoOrderDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperAdmissionBlockerEvent:
    event_id: str
    created_at_utc: str
    attempt_type: PaperAdmissionAttemptType
    status: PaperAdmissionBlockerStatus
    decision: PaperAdmissionBlockerDecision
    action: PaperAdmissionBlockerAction
    blocked: bool
    admission_allowed: bool
    active_paper_enabled: bool
    order_created: bool
    paper_state_mutated: bool
    broker_order_sent: bool
    telegram_real_sent: bool
    config_patched: bool
    source_component: Optional[str]
    payload_summary: dict[str, Any]
    risk_flags: list[NoOrderDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoOrderPaperSessionDossier:
    dossier_id: str
    created_at_utc: str
    status: NoOrderSessionDossierStatus
    decision: NoOrderSessionDossierDecision
    candidate_id: Optional[str]
    source_bridge_review_id: Optional[str]
    source_bridge_dry_run_id: Optional[str]
    source_no_order_session_id: Optional[str]
    source_bridge_replay_result_id: Optional[str]
    evidence_items: list[NoOrderDossierEvidenceItem]
    bridge_replay_audit_seal: Optional[BridgeReplayAuditSeal]
    blocker_events: list[PaperAdmissionBlockerEvent]
    evidence_refs: list[str]
    dossier_hash: Optional[str]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: list[NoOrderDossierRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoOrderDossierAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[NoOrderDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoOrderDossierFullReview:
    review_id: str
    created_at_utc: str
    report_type: NoOrderDossierReportType
    dossiers: list[NoOrderPaperSessionDossier]
    evidence_items: list[NoOrderDossierEvidenceItem]
    replay_audit_seals: list[BridgeReplayAuditSeal]
    blocker_rules: list[PaperAdmissionBlockerRule]
    blocker_events: list[PaperAdmissionBlockerEvent]
    audit_entries: list[NoOrderDossierAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

import uuid
from datetime import datetime, timezone

def create_no_order_evidence_id(prefix: str = "no_order_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_bridge_replay_audit_seal_id(prefix: str = "bridge_replay_audit_seal") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_admission_blocker_rule_id(prefix: str = "admission_blocker_rule") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_admission_blocker_event_id(prefix: str = "admission_blocker_event") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_no_order_dossier_id(prefix: str = "no_order_dossier") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_no_order_dossier_audit_id(prefix: str = "no_order_dossier_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_no_order_dossier_full_review_id(prefix: str = "no_order_dossier_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

from dataclasses import asdict

def no_order_dossier_evidence_item_to_dict(item: NoOrderDossierEvidenceItem) -> dict:
    return asdict(item)

def bridge_replay_audit_seal_to_dict(item: BridgeReplayAuditSeal) -> dict:
    return asdict(item)

def paper_admission_blocker_rule_to_dict(item: PaperAdmissionBlockerRule) -> dict:
    return asdict(item)

def paper_admission_blocker_event_to_dict(item: PaperAdmissionBlockerEvent) -> dict:
    return asdict(item)

def no_order_paper_session_dossier_to_dict(item: NoOrderPaperSessionDossier) -> dict:
    return asdict(item)

def no_order_dossier_audit_entry_to_dict(item: NoOrderDossierAuditEntry) -> dict:
    return asdict(item)

def no_order_dossier_full_review_to_dict(item: NoOrderDossierFullReview) -> dict:
    return asdict(item)

def validate_no_order_dossier_evidence_item(item: NoOrderDossierEvidenceItem) -> None:
    pass

def validate_bridge_replay_audit_seal(item: BridgeReplayAuditSeal) -> None:
    if item.sealed and not item.immutable:
        raise ValueError("If sealed is True, immutable must be True")
    if not item.all_dangerous_routes_denied:
        raise ValueError("all_dangerous_routes_denied must be True")
    if item.dangerous_allowed_count != 0:
        raise ValueError("dangerous_allowed_count must be 0")

def validate_paper_admission_blocker_rule(item: PaperAdmissionBlockerRule) -> None:
    if not item.enabled:
        raise ValueError("rule enabled must be True")
    if not item.blocking:
        raise ValueError("rule blocking must be True")

def validate_paper_admission_blocker_event(item: PaperAdmissionBlockerEvent) -> None:
    if not item.blocked:
        raise ValueError("blocked must be True")
    if item.admission_allowed:
        raise ValueError("admission_allowed must be False")
    if item.active_paper_enabled:
        raise ValueError("active_paper_enabled must be False")
    if item.order_created:
        raise ValueError("order_created must be False")
    if item.paper_state_mutated:
        raise ValueError("paper_state_mutated must be False")
    if item.broker_order_sent:
        raise ValueError("broker_order_sent must be False")
    if item.telegram_real_sent:
        raise ValueError("telegram_real_sent must be False")
    if item.config_patched:
        raise ValueError("config_patched must be False")

def validate_no_order_paper_session_dossier(item: NoOrderPaperSessionDossier) -> None:
    if item.sealed and not item.immutable:
        raise ValueError("If sealed is True, immutable must be True")
    if not item.manual_review_required:
        raise ValueError("manual_review_required must be True")
    if not item.activation_denied:
        raise ValueError("activation_denied must be True")
    if item.activation_allowed:
        raise ValueError("activation_allowed must be False")
    if item.admission_allowed:
        raise ValueError("admission_allowed must be False")
    if item.transition_allowed:
        raise ValueError("transition_allowed must be False")
    if not item.all_writes_blocked:
        raise ValueError("all_writes_blocked must be True")
    if item.order_created:
        raise ValueError("order_created must be False")
    if item.mutation_detected:
        raise ValueError("mutation_detected must be False")
    if item.allows_active_paper:
        raise ValueError("allows_active_paper must be False")
    if item.allows_broker_execution:
        raise ValueError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation:
        raise ValueError("allows_paper_state_mutation must be False")
    if item.allows_config_patch:
        raise ValueError("allows_config_patch must be False")
    if item.allows_telegram_real_send:
        raise ValueError("allows_telegram_real_send must be False")

def validate_no_order_dossier_full_review(item: NoOrderDossierFullReview) -> None:
    for d in item.dossiers:
        validate_no_order_paper_session_dossier(d)
    for s in item.replay_audit_seals:
        validate_bridge_replay_audit_seal(s)
    for r in item.blocker_rules:
        validate_paper_admission_blocker_rule(r)
    for e in item.blocker_events:
        validate_paper_admission_blocker_event(e)
