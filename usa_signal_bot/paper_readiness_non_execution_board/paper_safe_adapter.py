from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import NonExecutionBoardFullReview

def non_execution_board_evidence_from_paper_safe(payload: Dict[str, Any]) -> List[str]:
    return [payload.get("paper_safe_gate_dossiers", [{}])[0].get("gate_id")]

def paper_safe_supports_non_execution_board(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    if "paper_safe_gate_dossiers" not in payload:
        warnings.append("Missing paper_safe_gate_dossiers")
    return len(warnings) == 0, warnings

def attach_non_execution_board_hint_to_paper_safe_payload(payload: Dict[str, Any], review: NonExecutionBoardFullReview) -> Dict[str, Any]:
    payload["non_execution_board_hint"] = {
        "review_id": review.review_id,
        "decision": review.boards[0].decision.value if review.boards else None
    }
    return payload

def paper_safe_non_execution_board_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    hint = payload.get("non_execution_board_hint", {})
    return {
        "has_hint": bool(hint),
        "decision": hint.get("decision")
    }

def paper_safe_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = paper_safe_non_execution_board_summary(payload)
    return f"--- PAPER SAFE ADAPTER ---\nHas Hint: {summary['has_hint']}\nDecision: {summary['decision']}"
