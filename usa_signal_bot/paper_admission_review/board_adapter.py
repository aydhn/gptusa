from typing import Any, Dict, List, Tuple
import json

def admission_evidence_from_board(payload: Dict[str, Any]) -> List[str]:
    return [payload.get("board_evidence_ref")] if payload.get("board_evidence_ref") else []

def board_supports_admission_review(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_admission_hint_to_board_payload(payload: Dict[str, Any], report: Any) -> Dict[str, Any]:
    payload["admission_hint"] = "Admission review via board completed"
    return payload

def board_admission_review_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"admission_hint": payload.get("admission_hint")}

def board_adapter_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(board_admission_review_summary(payload), indent=2)
