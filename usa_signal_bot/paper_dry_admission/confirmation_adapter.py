from typing import Any, Tuple, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import DryAdmissionFullReview

def dry_admission_evidence_from_confirmation(payload: dict[str, Any]) -> List[str]:
    evidence = []
    if payload.get("confirmation_id"):
        evidence.append(f"confirmation_id:{payload['confirmation_id']}")
    if payload.get("decision"):
        evidence.append(f"confirmation_decision:{payload['decision']}")
    return evidence

def confirmation_supports_dry_admission(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    supported = True

    if payload.get("decision") not in ["PASS", "PASS_WITH_ACTIVATION_DENIED"]:
        reasons.append("Confirmation decision is not PASS or PASS_WITH_ACTIVATION_DENIED")
        supported = False

    return supported, reasons

def attach_dry_admission_hint_to_confirmation_payload(payload: dict[str, Any], review: DryAdmissionFullReview) -> dict[str, Any]:
    new_payload = payload.copy()
    new_payload["dry_admission_hint"] = {
        "review_id": review.review_id,
        "run_status": review.runs[-1].status.value if review.runs else "UNKNOWN",
        "message": "Dry admission rehearsal is available. This is not a live activation."
    }
    return new_payload

def confirmation_dry_admission_summary(payload: dict[str, Any]) -> dict[str, Any]:
    hint = payload.get("dry_admission_hint", {})
    supported, reasons = confirmation_supports_dry_admission(payload)
    return {
        "supported": supported,
        "reasons": reasons,
        "has_hint": bool(hint),
        "hint_message": hint.get("message")
    }

def confirmation_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = confirmation_dry_admission_summary(payload)
    lines = [
        f"Supports Dry Admission: {summary['supported']}",
        f"Has Hint: {summary['has_hint']}"
    ]
    if summary['reasons']:
        lines.append("Block Reasons:")
        for r in summary['reasons']:
            lines.append(f"  - {r}")
    if summary['has_hint']:
        lines.append(f"Hint: {summary['hint_message']}")
    return "\n".join(lines)
