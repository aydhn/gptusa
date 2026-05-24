from typing import Any

def ingest_simulator_gate_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    return {"ingested_simulator_gate_review": payload}

def extract_final_simulator_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("final_simulator_gate")

def extract_rehearsal_replay_result(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("rehearsal_replay_result")

def extract_dry_admission_evidence_freeze(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("dry_admission_evidence_freeze")

def extract_simulator_rules(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("simulator_rules", [])

def extract_simulator_assertions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("simulator_assertions", [])

def extract_simulator_candidate_id(payload: dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def extract_simulator_decision(payload: dict[str, Any]) -> str | None:
    gate = extract_final_simulator_gate(payload)
    if gate:
        return gate.get("decision")
    return payload.get("decision")

def simulator_gate_supports_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    gate = extract_final_simulator_gate(payload)
    if not gate:
        reasons.append("Missing final simulator gate")
        return False, reasons
    if gate.get("decision") != "PASS_TO_SIMULATOR_GATE_DOSSIER" and gate.get("status") != "VALIDATED_SIMULATOR_SAFE":
        reasons.append(f"Invalid simulator gate decision or status: {gate.get('decision')} / {gate.get('status')}")
        return False, reasons

    if payload.get("activation_allowed") or gate.get("activation_allowed"):
        reasons.append("activation_allowed is true")
    if payload.get("admission_allowed") or gate.get("admission_allowed"):
        reasons.append("admission_allowed is true")
    if payload.get("transition_allowed") or gate.get("transition_allowed"):
        reasons.append("transition_allowed is true")
    if payload.get("simulator_admission_allowed") or gate.get("simulator_admission_allowed"):
        reasons.append("simulator_admission_allowed is true")
    if payload.get("local_paper_simulator_allowed") or gate.get("local_paper_simulator_allowed"):
        reasons.append("local_paper_simulator_allowed is true")
    if payload.get("rehearsal_allowed") or gate.get("rehearsal_allowed"):
        reasons.append("rehearsal_allowed is true")
    if payload.get("paper_mode_rehearsal_allowed") or gate.get("paper_mode_rehearsal_allowed"):
        reasons.append("paper_mode_rehearsal_allowed is true")
    if payload.get("order_created") or gate.get("order_created"):
        reasons.append("order_created is true")
    if payload.get("mutation_detected") or gate.get("mutation_detected"):
        reasons.append("mutation_detected is true")

    replay = extract_rehearsal_replay_result(payload)
    if replay and replay.get("allowed_attempt_count", 0) > 0:
        reasons.append("Rehearsal replay allowed attempts > 0")

    freeze = extract_dry_admission_evidence_freeze(payload)
    if freeze and freeze.get("status") in ["FAILED", "STALE"]:
        reasons.append(f"Evidence freeze invalid: {freeze.get('status')}")

    if reasons:
        return False, reasons

    return True, ["Simulator gate supports dossier"]

def simulator_gate_ingestion_to_text(payload: dict[str, Any]) -> str:
    supports, reasons = simulator_gate_supports_dossier(payload)
    lines = [
        "--- Simulator Gate Ingestion ---",
        f"Supports Dossier: {supports}",
        f"Candidate ID: {extract_simulator_candidate_id(payload)}",
        f"Decision: {extract_simulator_decision(payload)}",
        "Reasons:"
    ]
    lines.extend([f"  - {r}" for r in reasons])
    return "\n".join(lines)
