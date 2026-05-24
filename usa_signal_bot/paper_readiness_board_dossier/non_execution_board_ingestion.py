from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PaperReadinessBoardDossierStatus

def ingest_non_execution_board_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    # Extract needed info and return a clean payload
    return {
        "non_execution_board": extract_non_execution_board(payload),
        "runtime_replay_result": extract_runtime_map_replay_result(payload),
        "seal_integrity_audit": extract_non_execution_seal_integrity_audit(payload),
        "board_gates": extract_non_execution_board_gates(payload),
        "board_assertions": extract_non_execution_board_assertions(payload),
        "candidate_id": extract_board_candidate_id(payload),
        "decision": extract_board_decision(payload)
    }

def extract_non_execution_board(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("non_execution_board") or payload.get("paper_readiness_non_execution_board")

def extract_runtime_map_replay_result(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("runtime_replay_result") or payload.get("runtime_map_replay_result")

def extract_non_execution_seal_integrity_audit(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("seal_integrity_audit") or payload.get("non_execution_seal_integrity_audit")

def extract_non_execution_board_gates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    board = extract_non_execution_board(payload)
    if board and "board_gates" in board:
        return board["board_gates"]
    return payload.get("board_gates", [])

def extract_non_execution_board_assertions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    board = extract_non_execution_board(payload)
    if board and "board_assertions" in board:
        return board["board_assertions"]
    return payload.get("board_assertions", [])

def extract_board_candidate_id(payload: dict[str, Any]) -> str | None:
    board = extract_non_execution_board(payload)
    if board and "candidate_id" in board:
        return board["candidate_id"]
    return payload.get("candidate_id")

def extract_board_decision(payload: dict[str, Any]) -> str | None:
    board = extract_non_execution_board(payload)
    if board and "decision" in board:
        return board["decision"]
    return payload.get("decision")

def non_execution_board_supports_board_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    missing = []
    if not extract_non_execution_board(payload):
        missing.append("non_execution_board")
    if not extract_runtime_map_replay_result(payload):
        missing.append("runtime_map_replay_result")
    if not extract_non_execution_seal_integrity_audit(payload):
        missing.append("non_execution_seal_integrity_audit")
    return len(missing) == 0, missing

def non_execution_board_ingestion_to_text(payload: dict[str, Any]) -> str:
    parts = []
    board = extract_non_execution_board(payload)
    if board:
        parts.append(f"Non-Execution Board ID: {board.get('board_id', 'Unknown')}")
        parts.append(f"Status: {board.get('status', 'Unknown')}")
        parts.append(f"Decision: {board.get('decision', 'Unknown')}")
    else:
        parts.append("Non-Execution Board: Missing")
    return "\n".join(parts)
