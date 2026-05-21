from typing import Any, Dict, List, Tuple

def promotion_evidence_from_controlled_planning_review(payload: Dict[str, Any]) -> List[str]:
    return ["controlled_planning_review"]

def controlled_planning_supports_promotion_dossier(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_promotion_dossier_to_controlled_planning_payload(payload: Dict[str, Any], review: Any) -> Dict[str, Any]:
    payload["promotion_dossier_review_id"] = getattr(review, "review_id", None)
    return payload

def controlled_planning_promotion_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"promotion_attached": "promotion_dossier_review_id" in payload}

def controlled_planning_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"Controlled Planning Adapter. Attached: {'promotion_dossier_review_id' in payload}."
