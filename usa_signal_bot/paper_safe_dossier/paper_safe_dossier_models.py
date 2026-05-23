from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid
import dataclasses

from usa_signal_bot.core.enums import (
    PaperSafeDossierStatus, PaperSafeDossierDecision,
    PaperSafeDossierEvidenceStatus, NonExecutionAcceptanceSealStatus,
    NonExecutionAcceptanceSealDecision, PrePaperRuntimeMapStatus,
    PrePaperRuntimeMapDecision, RuntimeComponentMode,
    RuntimeRoutePermission, PaperSafeDossierRiskFlag,
    PaperSafeDossierReportType
)

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class PaperSafeDossierEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    source_ref_id: Optional[str]
    source_path: Optional[str]
    status: PaperSafeDossierEvidenceStatus
    required: bool
    available: bool
    fresh: bool
    stale: bool
    summary: Dict[str, Any]
    risk_flags: List[PaperSafeDossierRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NonExecutionAcceptanceSeal:
    seal_id: str
    created_at_utc: str
    status: NonExecutionAcceptanceSealStatus
    decision: NonExecutionAcceptanceSealDecision
    candidate_id: Optional[str]
    source_paper_safe_gate_id: Optional[str]
    source_paper_safe_review_id: Optional[str]
    seal_hash: Optional[str]
    accepted_boundaries: List[str]
    sealed: bool
    immutable: bool
    non_execution_confirmed: bool
    no_broker_confirmed: bool
    no_active_paper_confirmed: bool
    no_paper_admission_confirmed: bool
    no_order_confirmed: bool
    no_write_confirmed: bool
    no_telegram_real_send_confirmed: bool
    no_config_patch_confirmed: bool
    seal_is_metadata_only: bool
    risk_flags: List[PaperSafeDossierRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeComponentMapItem:
    component_id: str
    created_at_utc: str
    component_name: str
    component_path: Optional[str]
    mode: RuntimeComponentMode
    read_only: bool
    preview_only: bool
    dry_run_only: bool
    write_allowed: bool
    order_allowed: bool
    broker_allowed: bool
    config_patch_allowed: bool
    telegram_real_send_allowed: bool
    activation_allowed: bool
    paper_admission_allowed: bool
    description: str
    risk_flags: List[PaperSafeDossierRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeRouteMapItem:
    route_id: str
    created_at_utc: str
    route_name: str
    source_component: Optional[str]
    target_component: Optional[str]
    permission: RuntimeRoutePermission
    read_only_allowed: bool
    preview_allowed: bool
    dry_run_allowed: bool
    write_allowed: bool
    order_allowed: bool
    broker_allowed: bool
    config_patch_allowed: bool
    telegram_real_send_allowed: bool
    activation_allowed: bool
    paper_admission_allowed: bool
    risk_flags: List[PaperSafeDossierRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PrePaperLocalRuntimeMap:
    runtime_map_id: str
    created_at_utc: str
    status: PrePaperRuntimeMapStatus
    decision: PrePaperRuntimeMapDecision
    candidate_id: Optional[str]
    source_paper_safe_gate_id: Optional[str]
    component_items: List[RuntimeComponentMapItem]
    route_items: List[RuntimeRouteMapItem]
    runtime_map_hash: Optional[str]
    map_is_metadata_only: bool
    read_only_boundary_confirmed: bool
    all_write_routes_denied: bool
    all_order_routes_denied: bool
    all_broker_routes_denied: bool
    all_config_patch_routes_denied: bool
    all_telegram_real_send_routes_denied: bool
    all_activation_routes_denied: bool
    all_paper_admission_routes_denied: bool
    risk_flags: List[PaperSafeDossierRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSafeGateDossier:
    dossier_id: str
    created_at_utc: str
    status: PaperSafeDossierStatus
    decision: PaperSafeDossierDecision
    candidate_id: Optional[str]
    source_paper_safe_review_id: Optional[str]
    source_paper_safe_gate_id: Optional[str]
    source_boundary_replay_result_id: Optional[str]
    source_integrity_audit_id: Optional[str]
    evidence_items: List[PaperSafeDossierEvidenceItem]
    non_execution_seal: Optional[NonExecutionAcceptanceSeal]
    runtime_map: Optional[PrePaperLocalRuntimeMap]
    evidence_refs: List[str]
    dossier_hash: Optional[str]
    sealed: bool
    immutable: bool
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    admission_allowed: bool
    transition_allowed: bool
    paper_safe_gate_passed: bool
    all_writes_blocked: bool
    order_created: bool
    mutation_detected: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: List[PaperSafeDossierRiskFlag]
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSafeDossierAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[PaperSafeDossierRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperSafeDossierFullReview:
    review_id: str
    created_at_utc: str
    report_type: PaperSafeDossierReportType
    dossiers: List[PaperSafeGateDossier]
    evidence_items: List[PaperSafeDossierEvidenceItem]
    non_execution_seals: List[NonExecutionAcceptanceSeal]
    runtime_maps: List[PrePaperLocalRuntimeMap]
    component_items: List[RuntimeComponentMapItem]
    route_items: List[RuntimeRouteMapItem]
    audit_entries: List[PaperSafeDossierAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]


def paper_safe_dossier_evidence_item_to_dict(item: PaperSafeDossierEvidenceItem) -> dict:
    return dataclasses.asdict(item)

def non_execution_acceptance_seal_to_dict(item: NonExecutionAcceptanceSeal) -> dict:
    return dataclasses.asdict(item)

def runtime_component_map_item_to_dict(item: RuntimeComponentMapItem) -> dict:
    return dataclasses.asdict(item)

def runtime_route_map_item_to_dict(item: RuntimeRouteMapItem) -> dict:
    return dataclasses.asdict(item)

def pre_paper_local_runtime_map_to_dict(item: PrePaperLocalRuntimeMap) -> dict:
    return dataclasses.asdict(item)

def paper_safe_gate_dossier_to_dict(item: PaperSafeGateDossier) -> dict:
    return dataclasses.asdict(item)

def paper_safe_dossier_audit_entry_to_dict(item: PaperSafeDossierAuditEntry) -> dict:
    return dataclasses.asdict(item)

def paper_safe_dossier_full_review_to_dict(item: PaperSafeDossierFullReview) -> dict:
    return dataclasses.asdict(item)

def validate_paper_safe_dossier_evidence_item(item: PaperSafeDossierEvidenceItem) -> None:
    pass

def validate_non_execution_acceptance_seal(item: NonExecutionAcceptanceSeal) -> None:
    if item.sealed and not item.immutable:
        item.immutable = True
    if not item.non_execution_confirmed or not item.no_broker_confirmed or not item.no_active_paper_confirmed:
        item.status = NonExecutionAcceptanceSealStatus.FAILED
    if not item.seal_is_metadata_only:
        item.seal_is_metadata_only = True

def validate_runtime_component_map_item(item: RuntimeComponentMapItem) -> None:
    if item.write_allowed or item.order_allowed or item.broker_allowed or item.config_patch_allowed or item.telegram_real_send_allowed or item.activation_allowed or item.paper_admission_allowed:
        item.warnings.append("Dangerous allowed flags detected in component.")

def validate_runtime_route_map_item(item: RuntimeRouteMapItem) -> None:
    if item.write_allowed or item.order_allowed or item.broker_allowed or item.config_patch_allowed or item.telegram_real_send_allowed or item.activation_allowed or item.paper_admission_allowed:
         item.warnings.append("Dangerous allowed flags detected in route.")

def validate_pre_paper_local_runtime_map(item: PrePaperLocalRuntimeMap) -> None:
    if not item.map_is_metadata_only:
        item.map_is_metadata_only = True
    for comp in item.component_items:
        validate_runtime_component_map_item(comp)
    for route in item.route_items:
        validate_runtime_route_map_item(route)

def validate_paper_safe_gate_dossier(item: PaperSafeGateDossier) -> None:
    if item.sealed and not item.immutable:
        item.immutable = True
    if not item.manual_review_required:
        item.manual_review_required = True
    if not item.activation_denied:
        item.activation_denied = True
    if item.activation_allowed:
        item.activation_allowed = False
    if item.admission_allowed:
        item.admission_allowed = False
    if item.transition_allowed:
        item.transition_allowed = False
    if not item.paper_safe_gate_passed:
        item.warnings.append("Paper safe gate not passed")
    if not item.all_writes_blocked:
        item.all_writes_blocked = True
    if item.order_created:
        item.order_created = False
    if item.mutation_detected:
        item.mutation_detected = False
    if item.allows_active_paper or item.allows_broker_execution or item.allows_paper_state_mutation or item.allows_config_patch or item.allows_telegram_real_send:
        item.allows_active_paper = False
        item.allows_broker_execution = False
        item.allows_paper_state_mutation = False
        item.allows_config_patch = False
        item.allows_telegram_real_send = False

def validate_paper_safe_dossier_full_review(item: PaperSafeDossierFullReview) -> None:
    for dossier in item.dossiers:
        validate_paper_safe_gate_dossier(dossier)
    for seal in item.non_execution_seals:
        validate_non_execution_acceptance_seal(seal)
    for map_item in item.runtime_maps:
        validate_pre_paper_local_runtime_map(map_item)

def create_paper_safe_dossier_evidence_id(prefix: str = "paper_safe_dossier_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_non_execution_seal_id(prefix: str = "non_execution_seal") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_runtime_component_id(prefix: str = "runtime_component") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_runtime_route_id(prefix: str = "runtime_route") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_pre_paper_runtime_map_id(prefix: str = "pre_paper_runtime_map") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_safe_dossier_id(prefix: str = "paper_safe_dossier") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_safe_dossier_audit_id(prefix: str = "paper_safe_dossier_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_safe_dossier_full_review_id(prefix: str = "paper_safe_dossier_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
