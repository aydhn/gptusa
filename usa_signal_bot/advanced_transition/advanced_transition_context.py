from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path
from usa_signal_bot.core.enums import AdvancedTransitionStatus, AdvancedTransitionDecision
from usa_signal_bot.advanced_transition.phase101_models import (
    AdvancedTransitionContext,
    HandoffFreezeIngestionResult,
    create_advanced_transition_context_id
)
from usa_signal_bot.advanced_transition.advanced_phase_roadmap import build_advanced_phase_roadmap
from usa_signal_bot.advanced_transition.module_inventory import build_module_inventory
from usa_signal_bot.advanced_transition.runtime_boundary_manifest import build_runtime_boundary_manifest

def build_advanced_transition_context(handoff: HandoffFreezeIngestionResult | None = None, project_root: Path | None = None, config: Dict[str, Any] | None = None) -> AdvancedTransitionContext:
    roadmap = build_advanced_phase_roadmap()
    inventory = build_module_inventory(project_root)
    boundary = build_runtime_boundary_manifest()

    handoff_valid = handoff is not None and handoff.valid_for_advanced_transition
    status = AdvancedTransitionStatus.VALIDATED if handoff_valid else AdvancedTransitionStatus.BLOCKED
    decision = AdvancedTransitionDecision.OPEN_ADVANCED_DEVELOPMENT_CONTEXT if handoff_valid else AdvancedTransitionDecision.BLOCK

    return AdvancedTransitionContext(
        context_id=create_advanced_transition_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        decision=decision,
        source_handoff_ingestion_id=handoff.ingestion_id if handoff else None,
        phase_start=101,
        phase_end=160,
        current_phase=101,
        final_phase=160,
        roadmap_items=roadmap,
        module_inventory=inventory,
        runtime_boundary_manifest=boundary,
        config_consolidated=True,
        storage_registry_ready=True,
        validation_registry_ready=True,
        health_registry_ready=True,
        cli_registry_ready=True,
        observability_registry_ready=True,
        notification_boundary_ready=True,
        advanced_transition_ready=handoff_valid,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_default_advanced_transition_context() -> AdvancedTransitionContext:
    from usa_signal_bot.advanced_transition.handoff_freeze_ingestion import ingest_handoff_freeze_payload
    handoff = ingest_handoff_freeze_payload({"frozen": True, "immutable": True, "handoff_is_metadata_only": True, "passed": True})
    return build_advanced_transition_context(handoff)

def advanced_transition_context_summary(context: AdvancedTransitionContext) -> Dict[str, Any]:
    return {"context_id": context.context_id, "status": context.status.name, "ready": context.advanced_transition_ready}

def advanced_transition_context_to_text(context: AdvancedTransitionContext, limit: int = 200) -> str:
    return f"Context ID: {context.context_id}\nStatus: {context.status.name}\nReady: {context.advanced_transition_ready}"
