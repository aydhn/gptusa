import datetime
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from usa_signal_bot.core.enums import (
    NoWriteTransitionDossierStatus,
    NoWriteTransitionDecision,
    TransitionDossierEvidenceStatus,
    AdmissionEvidenceSealValidationStatus,
    AdmissionEvidenceSealRefreshDecision,
    PaperSandboxBridgeStatus,
    PaperSandboxBridgeDecision,
    SandboxBridgeRouteStatus,
    SandboxBridgeRouteType,
    NoWriteTransitionRiskFlag,
    NoWriteTransitionReportType
)


@dataclass
class TransitionDossierEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    source_ref_id: Optional[str]
    source_path: Optional[str]
    status: TransitionDossierEvidenceStatus
    required: bool
    available: bool
    fresh: bool
    stale: bool
    summary: dict[str, Any]
    risk_flags: list[NoWriteTransitionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AdmissionEvidenceSealValidation:
    validation_id: str
    created_at_utc: str
    status: AdmissionEvidenceSealValidationStatus
    decision: AdmissionEvidenceSealRefreshDecision
    candidate_id: Optional[str]
    source_seal_id: Optional[str]
    expected_hash: Optional[str]
    observed_hash: Optional[str]
    hash_matches: bool
    sealed: bool
    immutable: bool
    evidence_ref_count: int
    missing_evidence_count: int
    stale_evidence_count: int
    risk_flags: list[NoWriteTransitionRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AdmissionEvidenceSealRefresh:
    refresh_id: str
    created_at_utc: str
    status: AdmissionEvidenceSealValidationStatus
    decision: AdmissionEvidenceSealRefreshDecision
    candidate_id: Optional[str]
    source_validation_id: Optional[str]
    refreshed_hash: Optional[str]
    refreshed_evidence_refs: list[str]
    sealed: bool
    immutable: bool
    refresh_is_metadata_only: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    risk_flags: list[NoWriteTransitionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PaperSandboxBridgeRoute:
    route_id: str
    created_at_utc: str
    route_type: SandboxBridgeRouteType
    status: SandboxBridgeRouteStatus
    read_only: bool
    write_allowed: bool
    order_allowed: bool
    broker_allowed: bool
    telegram_real_send_allowed: bool
    config_patch_allowed: bool
    activation_allowed: bool
    description: str
    risk_flags: list[NoWriteTransitionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PaperSandboxBridgeEnvelope:
    bridge_id: str
    created_at_utc: str
    status: PaperSandboxBridgeStatus
    decision: PaperSandboxBridgeDecision
    candidate_id: Optional[str]
    source_dossier_id: Optional[str]
    source_transition_checkpoint_id: Optional[str]
    source_evidence_seal_id: Optional[str]
    routes: list[PaperSandboxBridgeRoute]
    read_only_snapshot_hash: Optional[str]
    bridge_is_no_write: bool
    bridge_is_metadata_only: bool
    activation_denied: bool
    activation_allowed: bool
    transition_allowed: bool
    all_writes_blocked: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    risk_flags: list[NoWriteTransitionRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NoWriteTransitionDossier:
    dossier_id: str
    created_at_utc: str
    status: NoWriteTransitionDossierStatus
    decision: NoWriteTransitionDecision
    candidate_id: Optional[str]
    source_admission_report_id: Optional[str]
    source_admission_review_id: Optional[str]
    source_transition_checkpoint_id: Optional[str]
    source_evidence_seal_id: Optional[str]
    evidence_items: list[TransitionDossierEvidenceItem]
    evidence_seal_validation: Optional[AdmissionEvidenceSealValidation]
    evidence_seal_refresh: Optional[AdmissionEvidenceSealRefresh]
    bridge_envelope: Optional[PaperSandboxBridgeEnvelope]
    evidence_refs: list[str]
    dossier_hash: Optional[str]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    transition_allowed: bool
    all_writes_blocked: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: list[NoWriteTransitionRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NoWriteTransitionAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[NoWriteTransitionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NoWriteTransitionFullReview:
    review_id: str
    created_at_utc: str
    report_type: NoWriteTransitionReportType
    dossiers: list[NoWriteTransitionDossier]
    evidence_items: list[TransitionDossierEvidenceItem]
    seal_validations: list[AdmissionEvidenceSealValidation]
    seal_refreshes: list[AdmissionEvidenceSealRefresh]
    bridge_envelopes: list[PaperSandboxBridgeEnvelope]
    bridge_routes: list[PaperSandboxBridgeRoute]
    audit_entries: list[NoWriteTransitionAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]


def transition_dossier_evidence_item_to_dict(item: TransitionDossierEvidenceItem) -> dict:
    from usa_signal_bot.utils.serialization import dataclass_to_dict
    return dataclass_to_dict(item)

def admission_evidence_seal_validation_to_dict(item: AdmissionEvidenceSealValidation) -> dict:
    from usa_signal_bot.utils.serialization import dataclass_to_dict
    return dataclass_to_dict(item)

def admission_evidence_seal_refresh_to_dict(item: AdmissionEvidenceSealRefresh) -> dict:
    from usa_signal_bot.utils.serialization import dataclass_to_dict
    return dataclass_to_dict(item)

def paper_sandbox_bridge_route_to_dict(item: PaperSandboxBridgeRoute) -> dict:
    from usa_signal_bot.utils.serialization import dataclass_to_dict
    return dataclass_to_dict(item)

def paper_sandbox_bridge_envelope_to_dict(item: PaperSandboxBridgeEnvelope) -> dict:
    from usa_signal_bot.utils.serialization import dataclass_to_dict
    return dataclass_to_dict(item)

def no_write_transition_dossier_to_dict(item: NoWriteTransitionDossier) -> dict:
    from usa_signal_bot.utils.serialization import dataclass_to_dict
    return dataclass_to_dict(item)

def no_write_transition_audit_entry_to_dict(item: NoWriteTransitionAuditEntry) -> dict:
    from usa_signal_bot.utils.serialization import dataclass_to_dict
    return dataclass_to_dict(item)

def no_write_transition_full_review_to_dict(item: NoWriteTransitionFullReview) -> dict:
    from usa_signal_bot.utils.serialization import dataclass_to_dict
    return dataclass_to_dict(item)


def validate_transition_dossier_evidence_item(item: TransitionDossierEvidenceItem) -> None:
    pass

def validate_admission_evidence_seal_validation(item: AdmissionEvidenceSealValidation) -> None:
    if not item.sealed and item.immutable:
        raise ValueError("If immutable is true, sealed must be true.")

def validate_admission_evidence_seal_refresh(item: AdmissionEvidenceSealRefresh) -> None:
    if not item.refresh_is_metadata_only:
        raise ValueError("Evidence seal refresh must be metadata-only.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Evidence seal refresh cannot allow active paper, broker execution, paper state mutation, config patch, or real Telegram send.")
    if not item.sealed or not item.immutable:
         raise ValueError("Refresh must be sealed and immutable.")

def validate_paper_sandbox_bridge_route(item: PaperSandboxBridgeRoute) -> None:
    if item.write_allowed or item.order_allowed or item.broker_allowed or item.telegram_real_send_allowed or item.config_patch_allowed or item.activation_allowed:
        raise ValueError("Bridge route cannot allow write, order, broker, Telegram real send, config patch, or activation.")

def validate_paper_sandbox_bridge_envelope(item: PaperSandboxBridgeEnvelope) -> None:
    if not item.bridge_is_no_write:
        raise ValueError("Bridge envelope must be no-write.")
    if not item.bridge_is_metadata_only:
        raise ValueError("Bridge envelope must be metadata-only.")
    if not item.activation_denied:
        raise ValueError("Activation must be explicitly denied in the bridge envelope.")
    if item.activation_allowed:
        raise ValueError("Activation cannot be allowed in the bridge envelope.")
    if item.transition_allowed:
        raise ValueError("Transition cannot be allowed in the bridge envelope.")
    if not item.all_writes_blocked:
        raise ValueError("All writes must be blocked in the bridge envelope.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Bridge envelope cannot allow active paper, broker execution, paper state mutation, config patch, or real Telegram send.")
    for route in item.routes:
        validate_paper_sandbox_bridge_route(route)

def validate_no_write_transition_dossier(item: NoWriteTransitionDossier) -> None:
    if not item.activation_denied:
        raise ValueError("Dossier must explicitly deny activation.")
    if item.activation_allowed:
        raise ValueError("Dossier cannot allow activation.")
    if item.transition_allowed:
        raise ValueError("Dossier cannot allow transition.")
    if not item.all_writes_blocked:
        raise ValueError("Dossier must block all writes.")
    if item.mutation_detected:
        raise ValueError("Dossier cannot have mutation detected.")
    if not item.manual_review_required:
        raise ValueError("Dossier must require manual review.")
    if item.sealed and not item.immutable:
        raise ValueError("Sealed dossier must be immutable.")
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        raise ValueError("Dossier cannot allow active paper, broker execution, paper state mutation, config patch, or real Telegram send.")

def validate_no_write_transition_full_review(item: NoWriteTransitionFullReview) -> None:
    for dossier in item.dossiers:
        validate_no_write_transition_dossier(dossier)
    for seal_validation in item.seal_validations:
        validate_admission_evidence_seal_validation(seal_validation)
    for seal_refresh in item.seal_refreshes:
        validate_admission_evidence_seal_refresh(seal_refresh)
    for bridge_envelope in item.bridge_envelopes:
        validate_paper_sandbox_bridge_envelope(bridge_envelope)
    for route in item.bridge_routes:
        validate_paper_sandbox_bridge_route(route)


def create_transition_evidence_id(prefix: str = "transition_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_seal_validation_id(prefix: str = "evidence_seal_validation") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_seal_refresh_id(prefix: str = "evidence_seal_refresh") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_bridge_route_id(prefix: str = "sandbox_bridge_route") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_bridge_envelope_id(prefix: str = "sandbox_bridge") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_transition_dossier_id(prefix: str = "no_write_transition_dossier") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_transition_audit_id(prefix: str = "no_write_transition_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_transition_full_review_id(prefix: str = "no_write_transition_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

# Phase 90 integration stub

# Phase 90 integration
