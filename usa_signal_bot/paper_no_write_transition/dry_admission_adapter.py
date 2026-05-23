from typing import Any
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import NoWriteTransitionFullReview

def transition_evidence_from_dry_admission(payload: dict[str, Any]) -> list[str]:
    return ["dry_admission_evidence_mock"]

def dry_admission_supports_no_write_transition(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return True, []

def attach_transition_hint_to_dry_admission_payload(payload: dict[str, Any], review: NoWriteTransitionFullReview) -> dict[str, Any]:
    out = payload.copy()
    out["no_write_transition_hint"] = review.review_id
    return out

def dry_admission_transition_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "Dry Admission Adapter OK"}

def dry_admission_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Dry Admission Adapter Summary"
