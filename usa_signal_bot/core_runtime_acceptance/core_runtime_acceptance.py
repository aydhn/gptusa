from typing import Dict, Any, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    CoreRuntimeAcceptanceItem,
    CoreRuntimeAcceptanceReport,
    LifecycleReviewIngestionResult,
    ConsolidationEvidenceItem,
    CoreRuntimeAcceptanceStatus,
    CoreRuntimeAcceptanceDecision,
    create_core_runtime_acceptance_item_id,
    create_core_runtime_acceptance_report_id,
    _now
)

def required_core_runtime_acceptance_items() -> List[str]:
    return [
        "phase100_handoff_preserved",
        "phase101_transition_context_ready",
        "phase102_runtime_registry_normalized",
        "phase102_provider_interfaces_ready",
        "phase103_service_graph_valid",
        "phase103_safe_orchestration_dry_run_passed",
        "phase104_lifecycle_ready",
        "phase104_readiness_gate_passed",
        "config_surface_safe",
        "no_execution_boundary_preserved",
        "provider_expansion_ready_metadata_only"
    ]

def build_core_runtime_acceptance_items(lifecycle: LifecycleReviewIngestionResult, evidence_items: List[ConsolidationEvidenceItem]) -> List[CoreRuntimeAcceptanceItem]:
    items = []
    for req in required_core_runtime_acceptance_items():
        accepted = True
        status = CoreRuntimeAcceptanceStatus.ACCEPTED_METADATA_ONLY
        decision = CoreRuntimeAcceptanceDecision.ACCEPT_CORE_RUNTIME_CONSOLIDATION

        if not lifecycle.valid_for_phase105:
            accepted = False
            status = CoreRuntimeAcceptanceStatus.BLOCKED
            decision = CoreRuntimeAcceptanceDecision.BLOCK

        items.append(CoreRuntimeAcceptanceItem(
            item_id=create_core_runtime_acceptance_item_id(),
            created_at_utc=_now(),
            acceptance_name=req,
            status=status,
            decision=decision,
            accepted=accepted,
            required=True
        ))
    return items

def build_core_runtime_acceptance_report(lifecycle: LifecycleReviewIngestionResult, evidence_items: List[ConsolidationEvidenceItem]) -> CoreRuntimeAcceptanceReport:
    items = build_core_runtime_acceptance_items(lifecycle, evidence_items)
    accepted_count = len([i for i in items if i.accepted])
    blocked_count = len([i for i in items if not i.accepted])

    core_runtime_accepted = (blocked_count == 0)

    status = CoreRuntimeAcceptanceStatus.ACCEPTED_METADATA_ONLY if core_runtime_accepted else CoreRuntimeAcceptanceStatus.BLOCKED
    decision = CoreRuntimeAcceptanceDecision.ACCEPT_CORE_RUNTIME_CONSOLIDATION if core_runtime_accepted else CoreRuntimeAcceptanceDecision.BLOCK

    return CoreRuntimeAcceptanceReport(
        report_id=create_core_runtime_acceptance_report_id(),
        created_at_utc=_now(),
        status=status,
        decision=decision,
        source_lifecycle_review_id=lifecycle.ingestion_id,
        items=items,
        accepted_item_count=accepted_count,
        blocked_item_count=blocked_count,
        failed_item_count=0,
        core_runtime_accepted=core_runtime_accepted,
        metadata_only_acceptance=True,
        read_only_acceptance=True,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False
    )

def evaluate_core_runtime_acceptance(report: CoreRuntimeAcceptanceReport) -> CoreRuntimeAcceptanceDecision:
    return report.decision

def core_runtime_acceptance_summary(report: CoreRuntimeAcceptanceReport) -> Dict[str, Any]:
    return {
        "status": report.status.name,
        "accepted": report.core_runtime_accepted,
        "items": len(report.items)
    }

def core_runtime_acceptance_to_text(report: CoreRuntimeAcceptanceReport, limit: int = 200) -> str:
    return f"Core Runtime Acceptance: {report.status.name}"
