import os
from pathlib import Path

FILES = {}

FILES["usa_signal_bot/paper_observation/dry_run_ingestion.py"] = """\
from typing import Any, List

def extract_dry_run_sessions(payload: dict[str, Any]) -> List[dict[str, Any]]:
    return payload.get("sessions", [])

def extract_dry_run_session_ids(payload: dict[str, Any]) -> List[str]:
    sessions = extract_dry_run_sessions(payload)
    return [s.get("session_id") for s in sessions if "session_id" in s]

def extract_human_checkpoints(payload: dict[str, Any]) -> List[dict[str, Any]]:
    return payload.get("checkpoints", [])

def extract_bridge_telemetry_events(payload: dict[str, Any]) -> List[dict[str, Any]]:
    return payload.get("telemetry_events", [])

def dry_run_ingestion_warnings(payload: dict[str, Any]) -> List[str]:
    warnings = []
    if not extract_dry_run_sessions(payload):
        warnings.append("Missing dry-run sessions.")
    if payload.get("blocked_operation_count", 0) > 0:
        warnings.append("Blocked operations found in telemetry.")
    return warnings

def ingest_dry_run_bridge_review(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "sessions": extract_dry_run_sessions(payload),
        "session_ids": extract_dry_run_session_ids(payload),
        "checkpoints": extract_human_checkpoints(payload),
        "telemetry_events": extract_bridge_telemetry_events(payload),
        "warnings": dry_run_ingestion_warnings(payload),
        "metadata": {"ingested": True}
    }

def dry_run_ingestion_to_text(payload: dict[str, Any]) -> str:
    warnings = dry_run_ingestion_warnings(payload)
    w_str = "\\n".join(warnings) if warnings else "None"
    return f"Dry-run Bridge Review Ingestion\\nSessions: {len(extract_dry_run_sessions(payload))}\\nWarnings: {w_str}"
"""

FILES["usa_signal_bot/paper_observation/quarantine_ingestion.py"] = """\
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
    return f"Quarantine Ingestion\\nCandidate: {cand_id}\\nStatus: {status}\\nSupports Observation: {supports}"
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
