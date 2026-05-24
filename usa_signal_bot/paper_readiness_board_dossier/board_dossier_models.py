from dataclasses import dataclass, field
from typing import Any
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    PaperReadinessBoardDossierStatus,
    PaperReadinessBoardDossierDecision,
    BoardDossierEvidenceStatus,
    AcceptanceBoardSealStatus,
    AcceptanceBoardSealDecision,
    ShadowLaunchBlockerStatus,
    ShadowLaunchBlockerDecision,
    ShadowLaunchAttemptType,
    ShadowLaunchBlockerAction,
    BoardDossierRiskFlag,
    BoardDossierReportType,
)
from usa_signal_bot.core.exceptions import (
    BoardDossierValidationError,
    AcceptanceBoardSealValidationError,
    FinalShadowLaunchBlockerError,
)

@dataclass
class BoardDossierEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    status: BoardDossierEvidenceStatus
    required: bool
    available: bool
    fresh: bool
    stale: bool
    summary: dict[str, Any]
    risk_flags: list[BoardDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    source_ref_id: str | None = None
    source_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AcceptanceBoardSeal:
    seal_id: str
    created_at_utc: str
    status: AcceptanceBoardSealStatus
    decision: AcceptanceBoardSealDecision
    board_gates_passed: bool
    board_assertions_passed: bool
    runtime_replay_passed: bool
    all_dangerous_runtime_routes_denied: bool
    non_execution_seal_integrity_valid: bool
    sealed: bool
    immutable: bool
    seal_is_metadata_only: bool
    allows_shadow_launch: bool
    allows_paper_mode_launch: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    risk_flags: list[BoardDossierRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    accepted_boundaries: list[str] = field(default_factory=list)
    candidate_id: str | None = None
    source_board_id: str | None = None
    source_board_review_id: str | None = None
    source_runtime_replay_result_id: str | None = None
    source_seal_integrity_audit_id: str | None = None
    seal_hash: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowLaunchBlockerRule:
    rule_id: str
    created_at_utc: str
    attempt_type: ShadowLaunchAttemptType
    enabled: bool
    blocking: bool
    action: ShadowLaunchBlockerAction
    description: str
    risk_flags: list[BoardDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowLaunchBlockerEvent:
    event_id: str
    created_at_utc: str
    attempt_type: ShadowLaunchAttemptType
    status: ShadowLaunchBlockerStatus
    decision: ShadowLaunchBlockerDecision
    action: ShadowLaunchBlockerAction
    blocked: bool
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
    risk_flags: list[BoardDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    source_component: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperReadinessBoardDossier:
    dossier_id: str
    created_at_utc: str
    status: PaperReadinessBoardDossierStatus
    decision: PaperReadinessBoardDossierDecision
    evidence_items: list[BoardDossierEvidenceItem]
    shadow_launch_blocker_events: list[ShadowLaunchBlockerEvent]
    evidence_refs: list[str]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    shadow_launch_allowed: bool
    paper_mode_launch_allowed: bool
    paper_safe_dossier_valid: bool
    non_execution_board_valid: bool
    non_execution_confirmed: bool
    runtime_map_safe: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: list[BoardDossierRiskFlag]
    required_followups: list[str]
    warnings: list[str]
    errors: list[str]
    acceptance_board_seal: AcceptanceBoardSeal | None = None
    candidate_id: str | None = None
    source_non_execution_board_review_id: str | None = None
    source_non_execution_board_id: str | None = None
    source_runtime_replay_result_id: str | None = None
    source_seal_integrity_audit_id: str | None = None
    dossier_hash: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoardDossierAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[BoardDossierRiskFlag]
    warnings: list[str]
    errors: list[str]
    decision: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BoardDossierFullReview:
    review_id: str
    created_at_utc: str
    report_type: BoardDossierReportType
    dossiers: list[PaperReadinessBoardDossier]
    evidence_items: list[BoardDossierEvidenceItem]
    acceptance_board_seals: list[AcceptanceBoardSeal]
    shadow_launch_blocker_rules: list[ShadowLaunchBlockerRule]
    shadow_launch_blocker_events: list[ShadowLaunchBlockerEvent]
    audit_entries: list[BoardDossierAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

# Conversion Functions
def board_dossier_evidence_item_to_dict(item: BoardDossierEvidenceItem) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def acceptance_board_seal_to_dict(item: AcceptanceBoardSeal) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def shadow_launch_blocker_rule_to_dict(item: ShadowLaunchBlockerRule) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def shadow_launch_blocker_event_to_dict(item: ShadowLaunchBlockerEvent) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def paper_readiness_board_dossier_to_dict(item: PaperReadinessBoardDossier) -> dict[str, Any]:
    from usa_signal_bot.core.serialization import dataclass_to_dict
    return dataclass_to_dict(item)

def board_dossier_audit_entry_to_dict(item: BoardDossierAuditEntry) -> dict[str, Any]:
    from dataclasses import asdict
    return asdict(item)

def board_dossier_full_review_to_dict(item: BoardDossierFullReview) -> dict[str, Any]:
    from usa_signal_bot.core.serialization import dataclass_to_dict
    return dataclass_to_dict(item)


# ID Generators
def create_board_dossier_evidence_id(prefix: str = "board_dossier_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_acceptance_board_seal_id(prefix: str = "acceptance_board_seal") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_shadow_launch_blocker_rule_id(prefix: str = "shadow_launch_blocker_rule") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_shadow_launch_blocker_event_id(prefix: str = "shadow_launch_blocker_event") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_board_dossier_id(prefix: str = "paper_readiness_board_dossier") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_board_dossier_audit_id(prefix: str = "board_dossier_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_board_dossier_full_review_id(prefix: str = "board_dossier_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# Validation
def validate_board_dossier_evidence_item(item: BoardDossierEvidenceItem) -> None:
    pass

def validate_acceptance_board_seal(item: AcceptanceBoardSeal) -> None:
    if item.sealed and not item.immutable:
        raise AcceptanceBoardSealValidationError("sealed=True requires immutable=True")
    if not item.seal_is_metadata_only:
        raise AcceptanceBoardSealValidationError("seal_is_metadata_only must be True")
    if item.allows_shadow_launch:
        raise AcceptanceBoardSealValidationError("allows_shadow_launch must be False")
    if item.allows_paper_mode_launch:
        raise AcceptanceBoardSealValidationError("allows_paper_mode_launch must be False")
    if item.allows_active_paper:
        raise AcceptanceBoardSealValidationError("allows_active_paper must be False")
    if item.allows_broker_execution:
        raise AcceptanceBoardSealValidationError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation:
        raise AcceptanceBoardSealValidationError("allows_paper_state_mutation must be False")
    if item.allows_config_patch:
        raise AcceptanceBoardSealValidationError("allows_config_patch must be False")
    if item.allows_telegram_real_send:
        raise AcceptanceBoardSealValidationError("allows_telegram_real_send must be False")

def validate_shadow_launch_blocker_rule(item: ShadowLaunchBlockerRule) -> None:
    if not item.enabled:
        raise FinalShadowLaunchBlockerError("enabled must be True")
    if not item.blocking:
        raise FinalShadowLaunchBlockerError("blocking must be True")

def validate_shadow_launch_blocker_event(item: ShadowLaunchBlockerEvent) -> None:
    if not item.blocked:
        raise FinalShadowLaunchBlockerError("blocked must be True")
    if item.shadow_launch_allowed:
        raise FinalShadowLaunchBlockerError("shadow_launch_allowed must be False")
    if item.paper_mode_launch_allowed:
        raise FinalShadowLaunchBlockerError("paper_mode_launch_allowed must be False")
    if item.active_paper_enabled:
        raise FinalShadowLaunchBlockerError("active_paper_enabled must be False")
    if item.order_created:
        raise FinalShadowLaunchBlockerError("order_created must be False")
    if item.paper_state_mutated:
        raise FinalShadowLaunchBlockerError("paper_state_mutated must be False")
    if item.broker_order_sent:
        raise FinalShadowLaunchBlockerError("broker_order_sent must be False")
    if item.telegram_real_sent:
        raise FinalShadowLaunchBlockerError("telegram_real_sent must be False")
    if item.config_patched:
        raise FinalShadowLaunchBlockerError("config_patched must be False")

def validate_paper_readiness_board_dossier(item: PaperReadinessBoardDossier) -> None:
    if item.sealed and not item.immutable:
        raise BoardDossierValidationError("sealed=True requires immutable=True")
    if not item.manual_review_required:
        raise BoardDossierValidationError("manual_review_required must be True")
    if not item.activation_denied:
        raise BoardDossierValidationError("activation_denied must be True")
    if item.activation_allowed:
        raise BoardDossierValidationError("activation_allowed must be False")
    if item.admission_allowed:
        raise BoardDossierValidationError("admission_allowed must be False")
    if item.transition_allowed:
        raise BoardDossierValidationError("transition_allowed must be False")
    if item.shadow_launch_allowed:
        raise BoardDossierValidationError("shadow_launch_allowed must be False")
    if item.paper_mode_launch_allowed:
        raise BoardDossierValidationError("paper_mode_launch_allowed must be False")
    if not item.paper_safe_dossier_valid:
        raise BoardDossierValidationError("paper_safe_dossier_valid must be True")
    if not item.non_execution_board_valid:
        raise BoardDossierValidationError("non_execution_board_valid must be True")
    if not item.non_execution_confirmed:
        raise BoardDossierValidationError("non_execution_confirmed must be True")
    if not item.runtime_map_safe:
        raise BoardDossierValidationError("runtime_map_safe must be True")
    if not item.all_writes_blocked:
        raise BoardDossierValidationError("all_writes_blocked must be True")
    if item.order_created:
        raise BoardDossierValidationError("order_created must be False")
    if item.mutation_detected:
        raise BoardDossierValidationError("mutation_detected must be False")
    if item.allows_active_paper:
        raise BoardDossierValidationError("allows_active_paper must be False")
    if item.allows_broker_execution:
        raise BoardDossierValidationError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation:
        raise BoardDossierValidationError("allows_paper_state_mutation must be False")
    if item.allows_config_patch:
        raise BoardDossierValidationError("allows_config_patch must be False")
    if item.allows_telegram_real_send:
        raise BoardDossierValidationError("allows_telegram_real_send must be False")
    if item.acceptance_board_seal:
        validate_acceptance_board_seal(item.acceptance_board_seal)
    for event in item.shadow_launch_blocker_events:
        validate_shadow_launch_blocker_event(event)

def validate_board_dossier_full_review(item: BoardDossierFullReview) -> None:
    for dossier in item.dossiers:
        validate_paper_readiness_board_dossier(dossier)
    for seal in item.acceptance_board_seals:
        validate_acceptance_board_seal(seal)
    for rule in item.shadow_launch_blocker_rules:
        validate_shadow_launch_blocker_rule(rule)
    for event in item.shadow_launch_blocker_events:
        validate_shadow_launch_blocker_event(event)
