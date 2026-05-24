from dataclasses import dataclass, field
from typing import Any, List, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    AdvancedTransitionStatus,
    AdvancedTransitionDecision,
    AdvancedTransitionPhaseBand,
    RuntimeCapabilityStatus,
    RuntimeCapability,
    AdvancedTransitionRiskFlag,
    AdvancedTransitionReportType
)

@dataclass
class HandoffFreezeIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_gate_id: Optional[str]
    available: bool
    frozen: bool
    immutable: bool
    handoff_is_metadata_only: bool
    pre_paper_handoff_complete: bool
    activation_allowed: bool
    admission_allowed: bool
    active_paper_enabled: bool
    order_created: bool
    mutation_detected: bool
    valid_for_advanced_transition: bool
    risk_flags: List[AdvancedTransitionRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any]

@dataclass
class RuntimeCapabilityRecord:
    capability: RuntimeCapability
    status: RuntimeCapabilityStatus
    reason: str
    allowed_in_phase_101: bool
    requires_future_phase: bool
    risk_flags: List[AdvancedTransitionRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ModuleInventoryRecord:
    module_name: str
    package_path: str
    category: str
    exists: bool
    import_safe: bool
    has_tests: bool
    phase_band: AdvancedTransitionPhaseBand
    capabilities: List[RuntimeCapability]
    risk_flags: List[AdvancedTransitionRiskFlag]
    warnings: List[str]
    metadata: dict[str, Any]

@dataclass
class RuntimeBoundaryManifest:
    manifest_id: str
    created_at_utc: str
    allowed_capabilities: List[RuntimeCapabilityRecord]
    blocked_capabilities: List[RuntimeCapabilityRecord]
    read_only_capabilities: List[RuntimeCapabilityRecord]
    metadata_only_capabilities: List[RuntimeCapabilityRecord]
    all_execution_blocked: bool
    active_paper_blocked: bool
    broker_execution_blocked: bool
    paper_state_mutation_blocked: bool
    telegram_real_send_blocked: bool
    scraping_blocked: bool
    dashboard_blocked: bool
    risk_flags: List[AdvancedTransitionRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any]

@dataclass
class AdvancedPhaseRoadmapItem:
    phase_start: int
    phase_end: int
    band: AdvancedTransitionPhaseBand
    title: str
    objective: str
    allowed_scope: List[str]
    blocked_scope: List[str]
    output_expectation: List[str]
    metadata: dict[str, Any]

@dataclass
class AdvancedTransitionContext:
    context_id: str
    created_at_utc: str
    status: AdvancedTransitionStatus
    decision: AdvancedTransitionDecision
    source_handoff_ingestion_id: Optional[str]
    phase_start: int
    phase_end: int
    current_phase: int
    final_phase: int
    roadmap_items: List[AdvancedPhaseRoadmapItem]
    module_inventory: List[ModuleInventoryRecord]
    runtime_boundary_manifest: RuntimeBoundaryManifest
    config_consolidated: bool
    storage_registry_ready: bool
    validation_registry_ready: bool
    health_registry_ready: bool
    cli_registry_ready: bool
    observability_registry_ready: bool
    notification_boundary_ready: bool
    advanced_transition_ready: bool
    activation_allowed: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    dashboard_enabled: bool
    risk_flags: List[AdvancedTransitionRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any]

@dataclass
class AdvancedTransitionFullReview:
    review_id: str
    created_at_utc: str
    report_type: AdvancedTransitionReportType
    handoff_ingestion: HandoffFreezeIngestionResult
    context: AdvancedTransitionContext
    module_inventory: List[ModuleInventoryRecord]
    runtime_boundary_manifest: RuntimeBoundaryManifest
    roadmap_items: List[AdvancedPhaseRoadmapItem]
    output_paths: dict[str, str]
    warnings: List[str]
    errors: List[str]

def create_handoff_ingestion_id() -> str:
    return f"hfi_{uuid.uuid4().hex[:12]}"

def create_runtime_boundary_manifest_id() -> str:
    return f"rbm_{uuid.uuid4().hex[:12]}"

def create_advanced_transition_context_id() -> str:
    return f"atc_{uuid.uuid4().hex[:12]}"

def create_advanced_transition_full_review_id() -> str:
    return f"atfr_{uuid.uuid4().hex[:12]}"

def handoff_freeze_ingestion_result_to_dict(item: HandoffFreezeIngestionResult) -> dict:
    return item.__dict__

def runtime_capability_record_to_dict(item: RuntimeCapabilityRecord) -> dict:
    return item.__dict__

def module_inventory_record_to_dict(item: ModuleInventoryRecord) -> dict:
    return item.__dict__

def runtime_boundary_manifest_to_dict(item: RuntimeBoundaryManifest) -> dict:
    return item.__dict__

def advanced_phase_roadmap_item_to_dict(item: AdvancedPhaseRoadmapItem) -> dict:
    return item.__dict__

def advanced_transition_context_to_dict(item: AdvancedTransitionContext) -> dict:
    return item.__dict__

def advanced_transition_full_review_to_dict(item: AdvancedTransitionFullReview) -> dict:
    return item.__dict__

def validate_handoff_freeze_ingestion_result(item: HandoffFreezeIngestionResult) -> None:
    from usa_signal_bot.core.exceptions import AdvancedTransitionValidationError
    if not item.frozen:
        raise AdvancedTransitionValidationError("Handoff freeze must be frozen=True")
    if not item.immutable:
        raise AdvancedTransitionValidationError("Handoff freeze must be immutable=True")
    if not item.pre_paper_handoff_complete:
        raise AdvancedTransitionValidationError("pre_paper_handoff_complete must be True")
    if item.activation_allowed:
        raise AdvancedTransitionValidationError("activation_allowed must be False")
    if item.active_paper_enabled:
        raise AdvancedTransitionValidationError("active_paper_enabled must be False")

def validate_runtime_boundary_manifest(item: RuntimeBoundaryManifest) -> None:
    from usa_signal_bot.core.exceptions import AdvancedTransitionValidationError
    if not item.all_execution_blocked:
        raise AdvancedTransitionValidationError("all_execution_blocked must be True")
    if not item.active_paper_blocked:
        raise AdvancedTransitionValidationError("active_paper_blocked must be True")
    if not item.broker_execution_blocked:
        raise AdvancedTransitionValidationError("broker_execution_blocked must be True")
    if not item.paper_state_mutation_blocked:
        raise AdvancedTransitionValidationError("paper_state_mutation_blocked must be True")

def validate_advanced_transition_context(item: AdvancedTransitionContext) -> None:
    from usa_signal_bot.core.exceptions import AdvancedTransitionValidationError
    if item.phase_start != 101:
        raise AdvancedTransitionValidationError("phase_start must be 101")
    if item.final_phase != 160:
        raise AdvancedTransitionValidationError("final_phase must be 160")
    if item.current_phase != 101:
        raise AdvancedTransitionValidationError("current_phase must be 101")
    if item.activation_allowed:
        raise AdvancedTransitionValidationError("activation_allowed must be False")
    if item.active_paper_enabled:
        raise AdvancedTransitionValidationError("active_paper_enabled must be False")
    if item.broker_execution_enabled:
        raise AdvancedTransitionValidationError("broker_execution_enabled must be False")

def validate_advanced_transition_full_review(item: AdvancedTransitionFullReview) -> None:
    validate_handoff_freeze_ingestion_result(item.handoff_ingestion)
    validate_advanced_transition_context(item.context)
    validate_runtime_boundary_manifest(item.runtime_boundary_manifest)
