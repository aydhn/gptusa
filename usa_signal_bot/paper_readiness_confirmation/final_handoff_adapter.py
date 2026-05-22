from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import ReadinessConfirmationReview

def confirmation_evidence_from_final_handoff(payload: dict[str, Any]) -> list[str]:
    if payload and payload.get("review_id"):
        return [f"final_handoff_{payload['review_id']}"]
    return []

def final_handoff_supports_readiness_confirmation(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if payload.get("decision") != "APPROVE_FOR_ACTIVATION_DENIED_AUDIT":
        reasons.append("Final handoff did not approve for denied audit")
    return len(reasons) == 0, reasons

def attach_confirmation_hint_to_final_handoff_payload(payload: dict[str, Any], review: ReadinessConfirmationReview) -> dict[str, Any]:
    res = payload.copy()
    res["readiness_confirmation_hint"] = {
        "review_id": review.review_id
    }
    return res

def final_handoff_confirmation_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"has_final_handoff": bool(payload)}

def final_handoff_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Final Handoff Hint attached"
