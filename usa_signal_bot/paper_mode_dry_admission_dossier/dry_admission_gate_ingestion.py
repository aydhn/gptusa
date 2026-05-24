from typing import Any
import json

def ingest_dry_admission_gate_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    return payload

def extract_final_dry_admission_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("final_dry_admission_gate")

def extract_shadow_replay_result(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("shadow_replay_result")

def extract_board_evidence_freeze(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("board_evidence_freeze")

def extract_dry_admission_rules(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("dry_admission_rules", [])

def extract_dry_admission_assertions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("dry_admission_assertions", [])

def extract_dry_admission_candidate_id(payload: dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def extract_dry_admission_decision(payload: dict[str, Any]) -> str | None:
    return payload.get("decision")

def dry_admission_gate_supports_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []

    if payload.get("activation_allowed") is True:
        reasons.append("activation_allowed is true")
    if payload.get("admission_allowed") is True:
        reasons.append("admission_allowed is true")
    if payload.get("transition_allowed") is True:
        reasons.append("transition_allowed is true")
    if payload.get("shadow_launch_allowed") is True:
        reasons.append("shadow_launch_allowed is true")
    if payload.get("paper_mode_launch_allowed") is True:
        reasons.append("paper_mode_launch_allowed is true")
    if payload.get("order_created") is True:
        reasons.append("order_created is true")
    if payload.get("mutation_detected") is True:
        reasons.append("mutation_detected is true")

    shadow_replay = extract_shadow_replay_result(payload)
    if shadow_replay and shadow_replay.get("allowed_attempt_count", 0) > 0:
        reasons.append("shadow replay allowed_attempt_count > 0")

    freeze = extract_board_evidence_freeze(payload)
    if freeze and freeze.get("status") in ["FAILED", "STALE"]:
        reasons.append("evidence freeze failed or stale")

    gate = extract_final_dry_admission_gate(payload)
    if not gate:
        reasons.append("missing final dry-admission gate")

    supports = len(reasons) == 0
    return supports, reasons

def dry_admission_gate_ingestion_to_text(payload: dict[str, Any]) -> str:
    supports, reasons = dry_admission_gate_supports_dossier(payload)
    text = f"Dry-Admission Gate Ingestion:
"
    text += f"- Supports Dossier: {supports}
"
    if reasons:
        text += f"- Reasons: {', '.join(reasons)}
"
    return text
