from typing import Any, Tuple, List, Optional
from usa_signal_bot.core.enums import QuarantineCandidateStatus

def ingest_quarantine_review_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.copy()

def extract_quarantined_candidate_payload(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("candidate") or payload

def extract_quarantine_candidate_id(payload: dict[str, Any]) -> Optional[str]:
    candidate = extract_quarantined_candidate_payload(payload)
    if candidate:
        return candidate.get("candidate_id")
    return None

def extract_candidate_status(payload: dict[str, Any]) -> Optional[str]:
    candidate = extract_quarantined_candidate_payload(payload)
    if candidate:
        return candidate.get("status")
    return None

def quarantine_supports_dry_run_bridge(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    status = extract_candidate_status(payload)
    if not status:
        return False, ["Missing candidate status"]

    warnings = []
    if status == QuarantineCandidateStatus.ENROLLED.value:
        pass
    elif status == QuarantineCandidateStatus.READY_FOR_SUPERVISED_DRY_RUN.value:
        pass
    elif status in [
        QuarantineCandidateStatus.BLOCKED.value,
        QuarantineCandidateStatus.REJECTED.value,
        QuarantineCandidateStatus.EXPIRED.value
    ]:
        return False, [f"Candidate status {status} is not supported for dry run"]
    else:
        warnings.append(f"Candidate status {status} is not optimal for dry run")

    return True, warnings

def quarantine_ingestion_warnings(payload: dict[str, Any]) -> List[str]:
    _, warnings = quarantine_supports_dry_run_bridge(payload)
    return warnings

def quarantine_ingestion_to_text(payload: dict[str, Any]) -> str:
    status = extract_candidate_status(payload)
    candidate_id = extract_quarantine_candidate_id(payload)
    return f"Quarantine Ingestion: Candidate {candidate_id} (Status: {status})"
