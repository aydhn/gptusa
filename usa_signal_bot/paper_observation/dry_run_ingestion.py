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
    if any(e.get("event_type") == "BLOCKED_OPERATION" for e in extract_bridge_telemetry_events(payload)) or payload.get("blocked_operation_count", 0) > 0:
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
    w_str = "\n".join(warnings) if warnings else "None"
    return f"Dry-run Bridge Review Ingestion\nSessions: {len(extract_dry_run_sessions(payload))}\nWarnings: {w_str}"
