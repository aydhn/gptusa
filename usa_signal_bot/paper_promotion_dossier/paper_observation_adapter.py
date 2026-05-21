from typing import Any, Dict, List, Tuple

def promotion_evidence_from_observation_review(payload: Dict[str, Any]) -> List[str]:
    return ["observation_review"]

def observation_supports_promotion_dossier(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_promotion_dossier_to_observation_payload(payload: Dict[str, Any], review: Any) -> Dict[str, Any]:
    payload["promotion_dossier_review_id"] = getattr(review, "review_id", None)
    return payload

def paper_observation_promotion_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"promotion_attached": "promotion_dossier_review_id" in payload}

def paper_observation_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"Observation Adapter. Attached: {'promotion_dossier_review_id' in payload}."
