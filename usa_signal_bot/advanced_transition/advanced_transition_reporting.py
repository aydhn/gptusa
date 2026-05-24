from typing import Dict, Any
from usa_signal_bot.advanced_transition.phase101_models import (
    HandoffFreezeIngestionResult,
    RuntimeCapabilityRecord,
    ModuleInventoryRecord,
    RuntimeBoundaryManifest,
    AdvancedPhaseRoadmapItem,
    AdvancedTransitionContext,
    AdvancedTransitionFullReview
)

def handoff_freeze_ingestion_result_to_text(item: HandoffFreezeIngestionResult) -> str:
    from usa_signal_bot.advanced_transition.handoff_freeze_ingestion import handoff_freeze_ingestion_to_text
    return handoff_freeze_ingestion_to_text(item)

def runtime_capability_record_to_text(item: RuntimeCapabilityRecord) -> str:
    return f"{item.capability.name}: {item.status.name}"

def module_inventory_record_to_text(item: ModuleInventoryRecord) -> str:
    return f"{item.module_name}: {item.category}"

def runtime_boundary_manifest_to_text(item: RuntimeBoundaryManifest) -> str:
    from usa_signal_bot.advanced_transition.runtime_boundary_manifest import runtime_boundary_to_text
    return runtime_boundary_to_text(item)

def advanced_phase_roadmap_item_to_text(item: AdvancedPhaseRoadmapItem) -> str:
    return f"{item.phase_start}-{item.phase_end}: {item.band.name}"

def advanced_transition_context_to_text(item: AdvancedTransitionContext, limit: int = 200) -> str:
    from usa_signal_bot.advanced_transition.advanced_transition_context import advanced_transition_context_to_text
    return advanced_transition_context_to_text(item, limit)

def advanced_transition_full_review_to_text(item: AdvancedTransitionFullReview, limit: int = 300) -> str:
    from usa_signal_bot.advanced_transition.advanced_transition_report import advanced_transition_full_review_to_text
    return advanced_transition_full_review_to_text(item, limit)

def advanced_transition_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Reviews: {summary.get('reviews')}"

def advanced_transition_limitations_text() -> str:
    from usa_signal_bot.advanced_transition.advanced_transition_report import advanced_transition_limitations_text
    return advanced_transition_limitations_text()
