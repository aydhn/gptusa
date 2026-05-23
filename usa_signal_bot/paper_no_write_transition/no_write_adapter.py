from typing import Any
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import NoWriteTransitionFullReview

def transition_evidence_from_no_write_admission(payload: dict[str, Any]) -> list[str]:
    return ["no_write_admission_evidence_mock"]

def no_write_admission_supports_transition(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return True, []

def attach_transition_hint_to_no_write_payload(payload: dict[str, Any], review: NoWriteTransitionFullReview) -> dict[str, Any]:
    out = payload.copy()
    out["no_write_transition_hint"] = review.review_id
    return out

def no_write_transition_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "No Write Adapter OK"}

def no_write_adapter_to_text(payload: dict[str, Any]) -> str:
    return "No Write Adapter Summary"
