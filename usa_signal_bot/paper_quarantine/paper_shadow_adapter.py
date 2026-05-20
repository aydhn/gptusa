from typing import Any
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate

def quarantine_evidence_from_shadow_rehearsal(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "rehearsal_id": payload.get("rehearsal_id", "unknown"),
        "timestamp": payload.get("timestamp", "unknown"),
        "shadow_fills": len(payload.get("shadow_fills", [])),
    }

def shadow_rehearsal_supports_quarantine(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    if not payload.get("rehearsal_id"):
        return False, ["Missing rehearsal_id"]
    return True, []

def attach_quarantine_hint_to_shadow_rehearsal(payload: dict[str, Any], candidate: QuarantinedPaperCandidate) -> dict[str, Any]:
    payload["quarantine_candidate_id"] = candidate.candidate_id
    payload["quarantine_status"] = candidate.status.value
    return payload

def paper_shadow_quarantine_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": payload.get("quarantine_candidate_id"),
        "status": payload.get("quarantine_status"),
    }

def paper_shadow_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Paper Shadow Adapter\nCandidate: {payload.get('quarantine_candidate_id')}\nStatus: {payload.get('quarantine_status')}"
