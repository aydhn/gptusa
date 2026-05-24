from typing import Any

def ingest_dry_admission_dossier_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def extract_dry_admission_dossier(payload: dict[str, Any]) -> dict[str, Any] | None:
    return None

def extract_dry_admission_acceptance_seal(payload: dict[str, Any]) -> dict[str, Any] | None:
    return None

def extract_rehearsal_blocker_events(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return []

def extract_dry_admission_dossier_candidate_id(payload: dict[str, Any]) -> str | None:
    return None

def extract_dry_admission_dossier_decision(payload: dict[str, Any]) -> str | None:
    return None

def dry_admission_dossier_supports_simulator_gate(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return False, []

def dry_admission_dossier_ingestion_to_text(payload: dict[str, Any]) -> str:
    return ""
