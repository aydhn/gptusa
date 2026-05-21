from typing import Any

def ingest_paper_observer_review(payload: dict[str, Any]) -> dict[str, Any]:
    return payload

def extract_observer_sessions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("sessions", [])

def extract_latest_observer_session(payload: dict[str, Any]) -> dict[str, Any] | None:
    sessions = extract_observer_sessions(payload)
    return sessions[-1] if sessions else None

def extract_observer_outputs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("outputs", [])

def extract_observer_drift_events(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("drift_events", [])

def extract_observer_candidate_id(payload: dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def observer_ingestion_warnings(payload: dict[str, Any]) -> list[str]:
    warnings = []
    if not extract_observer_sessions(payload):
        warnings.append("Missing observer sessions.")
    if not payload.get("locked_runtime", True):
        warnings.append("Locked runtime is False. Unsafe!")
    return warnings

def observer_ingestion_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
