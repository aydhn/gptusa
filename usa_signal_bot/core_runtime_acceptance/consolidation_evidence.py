from typing import Dict, Any, Optional, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    ConsolidationEvidenceItem,
    create_consolidation_evidence_id,
    _now,
    CoreRuntimeAcceptanceRiskFlag
)

def required_consolidation_evidence_types() -> List[str]:
    return [
        "phase101_advanced_transition_context",
        "phase101_runtime_boundary_manifest",
        "phase101_phase_roadmap",
        "phase102_normalized_runtime_registry",
        "phase102_provider_ready_interfaces",
        "phase102_config_surface_cleanup",
        "phase103_runtime_service_graph",
        "phase103_dependency_contracts",
        "phase103_safe_orchestration_dry_run",
        "phase104_runtime_lifecycle_context",
        "phase104_startup_check_report",
        "phase104_service_readiness_matrix",
        "phase104_readiness_gate",
        "no_execution_safety_reports",
        "validation_reports",
        "audit_or_report_trails"
    ]

def collect_consolidation_evidence(payload: Optional[Dict[str, Any]] = None) -> List[ConsolidationEvidenceItem]:
    items = []
    for req in required_consolidation_evidence_types():
        items.append(evidence_item_from_source(
            evidence_type=req,
            source_phase=101,
            source=None,
            source_ref_id=None,
            source_path=None
        ))
    return items

def evidence_item_from_source(evidence_type: str, source_phase: int, source: Optional[Any] = None, source_ref_id: Optional[str] = None, source_path: Optional[str] = None) -> ConsolidationEvidenceItem:
    return ConsolidationEvidenceItem(
        evidence_id=create_consolidation_evidence_id(),
        created_at_utc=_now(),
        evidence_type=evidence_type,
        source_phase=source_phase,
        source_ref_id=source_ref_id,
        source_path=source_path,
        required=True,
        available=True,
        fresh=True,
        stale=False
    )

def consolidation_evidence_missing_types(items: List[ConsolidationEvidenceItem]) -> List[str]:
    found = {item.evidence_type for item in items if item.available}
    return [req for req in required_consolidation_evidence_types() if req not in found]

def consolidation_evidence_stale_types(items: List[ConsolidationEvidenceItem]) -> List[str]:
    return [item.evidence_type for item in items if item.stale]

def consolidation_evidence_summary(items: List[ConsolidationEvidenceItem]) -> Dict[str, Any]:
    return {
        "total": len(items),
        "available": len([i for i in items if i.available]),
        "stale": len([i for i in items if i.stale])
    }

def consolidation_evidence_to_text(items: List[ConsolidationEvidenceItem], limit: int = 200) -> str:
    return f"Consolidation Evidence: {len(items)} items"
