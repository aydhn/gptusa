from typing import Any
from .observer_governance_models import PromotionEvidenceItem, ObserverGovernanceReview

def evidence_from_controlled_planning_review(payload: dict[str, Any]) -> list[PromotionEvidenceItem]:
    return []

def controlled_planning_supports_observer_governance(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return True, []

def attach_observer_governance_to_controlled_planning_payload(payload: dict[str, Any], review: ObserverGovernanceReview) -> dict[str, Any]:
    payload["governance_review_id"] = review.review_id
    return payload

def controlled_planning_observer_governance_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"governance_review_id": payload.get("governance_review_id")}

def controlled_planning_adapter_to_text(payload: dict[str, Any]) -> str:
    return str(controlled_planning_observer_governance_summary(payload))
