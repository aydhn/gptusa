from typing import Any
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantineEnrollmentReview

def sandbox_payload_quarantine_refs(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": payload.get("quarantine_candidate_id"),
        "ticket_id": payload.get("promotion_ticket_id"),
        "bridge_plan_id": payload.get("bridge_plan_id")
    }

def sandbox_supports_quarantine(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    if not payload.get("sandbox_run_id"):
        return False, ["Missing sandbox_run_id"]
    return True, []

def attach_quarantine_metadata_to_sandbox_payload(payload: dict[str, Any], review: QuarantineEnrollmentReview) -> dict[str, Any]:
    if review.candidates:
        payload["quarantine_candidate_id"] = review.candidates[0].candidate_id
    if review.tickets:
        payload["promotion_ticket_id"] = review.tickets[0].ticket_id
    if review.bridge_plans:
        payload["bridge_plan_id"] = review.bridge_plans[0].bridge_plan_id
    return payload

def release_sandbox_quarantine_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return sandbox_payload_quarantine_refs(payload)

def release_sandbox_adapter_to_text(payload: dict[str, Any]) -> str:
    refs = sandbox_payload_quarantine_refs(payload)
    return f"Sandbox Quarantine Adapter\nRefs: {refs}"
