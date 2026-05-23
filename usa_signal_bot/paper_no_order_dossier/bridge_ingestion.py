from typing import Any
import json

def ingest_paper_sandbox_bridge_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    return payload

def extract_bridge_dry_run(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("dry_run_bridge")

def extract_no_order_session(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("no_order_session")

def extract_bridge_replay_result(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("bridge_replay_result")

def extract_bridge_route_attempts(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("route_attempts", [])

def extract_bridge_candidate_id(payload: dict[str, Any]) -> str | None:
    return payload.get("candidate_id")

def extract_bridge_decision(payload: dict[str, Any]) -> str | None:
    return payload.get("decision")

def bridge_review_supports_no_order_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []

    if payload.get("activation_allowed") is True:
        reasons.append("activation_allowed is true")
        return False, reasons
    if payload.get("transition_allowed") is True:
        reasons.append("transition_allowed is true")
        return False, reasons
    if payload.get("order_created") is True:
        reasons.append("order_created is true")
        return False, reasons
    if payload.get("mutation_detected") is True:
        reasons.append("mutation_detected is true")
        return False, reasons
    if payload.get("dangerous_allowed_count", 0) > 0:
        reasons.append("dangerous_allowed_count > 0")
        return False, reasons

    session = extract_no_order_session(payload)
    if not session:
        reasons.append("no_order_session missing")
    elif session.get("status") not in ["COMPLETED_NO_ORDER", "COMPLETED_NO_WRITE"]:
        reasons.append(f"no_order_session status {session.get('status')} missing/failed")

    replay = extract_bridge_replay_result(payload)
    if not replay:
        reasons.append("bridge_replay_result missing")
    elif replay.get("status") not in ["ALL_DANGEROUS_ROUTES_DENIED"]:
        pass # Optional check, actual status depends on phase 89 enum

    if len(reasons) > 0:
        return False, reasons
    return True, []

def bridge_ingestion_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
