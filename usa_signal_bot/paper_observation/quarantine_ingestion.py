from typing import Any, Tuple, List

def extract_candidate_id_from_quarantine(payload: dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def extract_ticket_id_from_quarantine(payload: dict[str, Any]) -> str | None:
    return payload.get("ticket_id")

def extract_quarantine_status(payload: dict[str, Any]) -> str | None:
    return payload.get("status")

def quarantine_payload_supports_observation(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    status = extract_quarantine_status(payload)
    if status in ["BLOCKED", "REJECTED", "EXPIRED"]:
        return False, [f"Quarantine status {status} blocks observation."]
    if status in ["ENROLLED", "READY_FOR_SUPERVISED_DRY_RUN"]:
        return True, []
    return False, ["Status does not clearly support observation."]

def ingest_quarantine_payload(payload: dict[str, Any]) -> dict[str, Any]:
    supports, reasons = quarantine_payload_supports_observation(payload)
    return {
        "candidate_id": extract_candidate_id_from_quarantine(payload),
        "ticket_id": extract_ticket_id_from_quarantine(payload),
        "status": extract_quarantine_status(payload),
        "supports_observation": supports,
        "reasons": reasons
    }

def quarantine_ingestion_to_text(payload: dict[str, Any]) -> str:
    cand_id = extract_candidate_id_from_quarantine(payload) or "Unknown"
    status = extract_quarantine_status(payload) or "Unknown"
    supports, _ = quarantine_payload_supports_observation(payload)
    return f"Quarantine Ingestion\nCandidate: {cand_id}\nStatus: {status}\nSupports Observation: {supports}"
