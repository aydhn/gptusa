from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def build_read_only_paper_observation_snapshot(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "read_only": True,
        "paper_state_committed": False,
        "paper_order_executed": False,
        "portfolio_state_mutated": False
    }

def compare_observation_to_paper_snapshot(review: ObservationReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"diff": "No real difference, paper is read only."}

def validate_paper_snapshot_not_mutated_for_observation(before: dict[str, Any], after: dict[str, Any]) -> List[str]:
    errors = []
    if after.get("paper_state_committed"):
        errors.append("paper_state_committed is True")
    if after.get("paper_order_executed"):
        errors.append("paper_order_executed is True")
    if after.get("portfolio_state_mutated"):
        errors.append("portfolio_state_mutated is True")
    return errors

def attach_observation_metadata_to_paper_analytics(payload: dict[str, Any], review: ObservationReview) -> dict[str, Any]:
    payload["observation_metadata"] = {"review_id": review.review_id}
    return payload

def paper_runtime_observation_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Paper Runtime Adapter Info"
