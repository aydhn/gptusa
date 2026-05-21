from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import ReadinessRehearsalReview

def handoff_evidence_from_observer_governance(payload: Dict[str, Any]) -> List[str]:
    return ["observer_governance_review"] if payload else []

def observer_governance_supports_readiness_rehearsal(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not payload:
        return False, ["Missing observer governance payload."]

    decision = payload.get("decision")
    if decision == "ELIGIBLE_FOR_NON_EXECUTING_PROMOTION_DOSSIER":
        return True, ["Observer governance passes."]

    return False, ["Observer governance decision not eligible."]

def attach_readiness_rehearsal_hint_to_observer_governance(payload: Dict[str, Any], review: ReadinessRehearsalReview) -> Dict[str, Any]:
    new_payload = payload.copy()
    new_payload["readiness_rehearsal_hint"] = {
        "review_id": review.review_id
    }
    return new_payload

def observer_governance_readiness_rehearsal_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    hint = payload.get("readiness_rehearsal_hint", {})
    return {"has_hint": bool(hint), "review_id": hint.get("review_id")}

def observer_governance_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = observer_governance_readiness_rehearsal_summary(payload)
    return f"Observer Governance Adapter: Has Hint={summary['has_hint']}"
