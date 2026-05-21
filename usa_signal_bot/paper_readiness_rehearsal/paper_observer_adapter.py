from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import ReadinessRehearsalReview

def handoff_evidence_from_paper_observer(payload: Dict[str, Any]) -> List[str]:
    return ["paper_observer_review"] if payload else []

def paper_observer_supports_readiness_rehearsal(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not payload:
        return False, ["Missing paper observer payload."]
    return True, ["Paper observer provides baseline data."]

def attach_readiness_rehearsal_hint_to_paper_observer(payload: Dict[str, Any], review: ReadinessRehearsalReview) -> Dict[str, Any]:
    new_payload = payload.copy()
    new_payload["readiness_rehearsal_hint"] = {
        "review_id": review.review_id
    }
    return new_payload

def paper_observer_readiness_rehearsal_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    hint = payload.get("readiness_rehearsal_hint", {})
    return {"has_hint": bool(hint), "review_id": hint.get("review_id")}

def paper_observer_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = paper_observer_readiness_rehearsal_summary(payload)
    return f"Paper Observer Adapter: Has Hint={summary['has_hint']}"
