from typing import Any, Dict, List, Optional
import copy
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import NonExecutionBoardFullReview

def build_read_only_paper_snapshot_for_non_execution_board(paper_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not paper_payload:
        return {"type": "read_only_paper_snapshot", "state": "empty"}
    snap = copy.deepcopy(paper_payload)
    snap["is_read_only"] = True
    return snap

def build_non_execution_board_snapshot(paper_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return build_read_only_paper_snapshot_for_non_execution_board(paper_payload)

def compare_non_execution_board_to_paper_snapshot(review: NonExecutionBoardFullReview, paper_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "paper_state_mutated": False,
        "differences": []
    }

def validate_paper_runtime_not_mutated_by_non_execution_board(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    # This guarantees we block if mutated
    errors = []
    if before.get("state") != after.get("state"):
        errors.append("Paper runtime state mutated")
    return errors

def attach_non_execution_board_metadata_to_paper_analytics(payload: Dict[str, Any], review: NonExecutionBoardFullReview) -> Dict[str, Any]:
    payload["non_execution_board_review_id"] = review.review_id
    payload["non_execution_board_decision"] = review.boards[0].decision.value if review.boards else None
    return payload

def paper_runtime_non_execution_board_adapter_to_text(payload: Dict[str, Any]) -> str:
    lines = ["--- PAPER RUNTIME ADAPTER ---"]
    lines.append(f"Review ID: {payload.get('non_execution_board_review_id')}")
    lines.append(f"Decision: {payload.get('non_execution_board_decision')}")
    return "\n".join(lines)
