from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import ReadinessConfirmationReview

def confirmation_evidence_from_pre_rehearsal(payload: dict[str, Any]) -> list[str]:
    if payload and payload.get("review_id"):
        return [f"pre_rehearsal_{payload['review_id']}"]
    return []

def pre_rehearsal_supports_readiness_confirmation(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if payload.get("status") != "PASSED":
        reasons.append("Pre rehearsal did not pass")
    return len(reasons) == 0, reasons

def attach_confirmation_hint_to_pre_rehearsal_payload(payload: dict[str, Any], review: ReadinessConfirmationReview) -> dict[str, Any]:
    res = payload.copy()
    res["readiness_confirmation_hint"] = {
        "review_id": review.review_id
    }
    return res

def pre_rehearsal_confirmation_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"has_pre_rehearsal": bool(payload)}

def pre_rehearsal_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Pre Rehearsal Hint attached"
