from typing import Any, Dict, Tuple, List
from usa_signal_bot.paper_observer.observer_models import PaperObserverReview

def observer_requirements_from_observation_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "requires_human_approval": True,
        "requires_planning_ticket": True,
        "requires_locked_runtime": True
    }

def observation_supports_observer_enrollment(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    # Just mock check
    if payload.get("status") == "REJECTED":
        warnings.append("Observation status is REJECTED")
        return False, warnings
    return True, warnings

def attach_observer_hint_to_observation_payload(payload: Dict[str, Any], review: PaperObserverReview) -> Dict[str, Any]:
    payload["paper_observer_hint"] = {
        "review_id": review.review_id,
        "sessions": len(review.sessions)
    }
    return payload

def paper_observation_observer_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("paper_observer_hint", {})

def paper_observation_adapter_to_text(payload: Dict[str, Any]) -> str:
    hint = payload.get("paper_observer_hint", {})
    return f"Observation adapter hint attached. Review ID: {hint.get('review_id')}"
