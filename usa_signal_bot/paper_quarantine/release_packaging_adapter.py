from typing import Any
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantineEnrollmentReview

def bundle_payload_quarantine_refs(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": payload.get("quarantine_candidate_id"),
        "status": payload.get("quarantine_status"),
    }

def bundle_supports_quarantine(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    if not payload.get("bundle_id"):
        return False, ["Missing bundle_id"]
    return True, []

def attach_quarantine_metadata_to_bundle_payload(payload: dict[str, Any], review: QuarantineEnrollmentReview) -> dict[str, Any]:
    if review.candidates:
        payload["quarantine_candidate_id"] = review.candidates[0].candidate_id
        payload["quarantine_status"] = review.candidates[0].status.value
    return payload

def release_packaging_quarantine_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return bundle_payload_quarantine_refs(payload)

def release_packaging_adapter_to_text(payload: dict[str, Any]) -> str:
    refs = bundle_payload_quarantine_refs(payload)
    return f"Packaging Quarantine Adapter\nRefs: {refs}"
