from typing import Any
from .observer_governance_models import ObserverGovernanceReview

def build_read_only_paper_snapshot_for_observer_governance(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    snap = (paper_payload or {}).copy()
    snap["paper_state_committed"] = False
    snap["paper_order_executed"] = False
    return snap

def compare_governance_observer_to_paper_snapshot(review: ObserverGovernanceReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"review_id": review.review_id, "snapshot_id": paper_snapshot.get("snapshot_id")}

def validate_paper_runtime_not_mutated_by_observer_governance(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    errors = []
    if before.get("paper_state_committed") != after.get("paper_state_committed"):
        errors.append("paper_state_committed mutated")
    return errors

def attach_observer_governance_metadata_to_paper_analytics(payload: dict[str, Any], review: ObserverGovernanceReview) -> dict[str, Any]:
    payload["governance_review_id"] = review.review_id
    return payload

def paper_runtime_observer_governance_adapter_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
