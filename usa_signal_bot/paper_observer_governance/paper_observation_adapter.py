from typing import Any
from .observer_governance_models import PromotionEvidenceItem, ObserverGovernanceReview

def evidence_from_observation_review(payload: dict[str, Any]) -> list[PromotionEvidenceItem]:
    return []

def observation_supports_observer_governance(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return True, []

def attach_observer_governance_to_observation_payload(payload: dict[str, Any], review: ObserverGovernanceReview) -> dict[str, Any]:
    payload["governance_review_id"] = review.review_id
    return payload

def paper_observation_observer_governance_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"governance_review_id": payload.get("governance_review_id")}

def paper_observation_adapter_to_text(payload: dict[str, Any]) -> str:
    return str(paper_observation_observer_governance_summary(payload))
