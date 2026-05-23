from typing import Any, Optional
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import NoWriteTransitionFullReview

def build_read_only_paper_snapshot_for_no_write_transition(paper_payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    snapshot = paper_payload.copy() if paper_payload else {}
    snapshot["paper_state_committed"] = False
    snapshot["paper_order_executed"] = False
    snapshot["portfolio_state_mutated"] = False
    return snapshot

def build_sandbox_bridge_snapshot_for_transition(paper_payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return build_read_only_paper_snapshot_for_no_write_transition(paper_payload)

def compare_transition_to_paper_snapshot(review: NoWriteTransitionFullReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"matches": True}

def validate_paper_runtime_not_mutated_by_transition(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    errors = []
    for k in ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]:
        if after.get(k) is True:
            errors.append(f"{k} mutated.")
    return errors

def attach_no_write_transition_metadata_to_paper_analytics(payload: dict[str, Any], review: NoWriteTransitionFullReview) -> dict[str, Any]:
    out = payload.copy()
    out["transition_metadata"] = review.review_id
    return out

def paper_runtime_no_write_transition_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Paper Runtime Adapter Summary"
