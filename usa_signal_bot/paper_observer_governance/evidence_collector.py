from typing import Any
from .observer_governance_models import PromotionEvidenceItem, create_promotion_evidence_item_id
from usa_signal_bot.core.enums import EvidenceFreshnessStatus
from datetime import datetime, timezone

def collect_promotion_evidence_items(observer_payload: dict[str, Any] | None = None, controlled_planning_payload: dict[str, Any] | None = None, observation_payload: dict[str, Any] | None = None) -> list[PromotionEvidenceItem]:
    items = []
    items.append(evidence_item_from_payload("observer_review", observer_payload))
    items.append(evidence_item_from_payload("controlled_planning_ticket", controlled_planning_payload))
    items.append(evidence_item_from_payload("observation_exit_review", observation_payload))
    for req in required_promotion_evidence_types():
        if not any(i.evidence_type == req for i in items):
            items.append(evidence_item_from_payload(req, None))
    return items

def required_promotion_evidence_types() -> list[str]:
    return [
        "observer_review", "observer_runtime_session", "observer_vs_paper_comparison",
        "controlled_planning_ticket", "final_human_approval_queue", "observation_exit_review",
        "dry_run_bridge_review", "quarantine_enrollment_review", "shadow_governance_review", "release_sandbox_review"
    ]

def evidence_item_from_payload(evidence_type: str, payload: dict[str, Any] | None, source_phase: str | None = None, source_ref_id: str | None = None) -> PromotionEvidenceItem:
    available = payload is not None and len(payload) > 0
    return PromotionEvidenceItem(
        evidence_id=create_promotion_evidence_item_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        evidence_type=evidence_type, source_phase=source_phase, source_ref_id=source_ref_id,
        status=EvidenceFreshnessStatus.FRESH if available else EvidenceFreshnessStatus.MISSING,
        summary={}, required=True, available=available, fresh=available, warnings=[], errors=[]
    )

def evidence_collection_summary(items: list[PromotionEvidenceItem]) -> dict[str, Any]:
    return {"total": len(items), "available": sum(1 for i in items if i.available)}

def evidence_collector_to_text(items: list[PromotionEvidenceItem], limit: int = 100) -> str:
    return str(evidence_collection_summary(items))
