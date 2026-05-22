from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import ReadinessConfirmationReview

def build_read_only_paper_snapshot_for_readiness_confirmation(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not paper_payload:
        return {}
    res = paper_payload.copy()
    res["is_read_only_snapshot"] = True
    return res

def compare_readiness_confirmation_to_paper_snapshot(review: ReadinessConfirmationReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "paper_id": paper_snapshot.get("paper_id")
    }

def validate_paper_runtime_not_mutated_by_readiness_confirmation(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    errors = []
    if before != after:
        errors.append("Paper runtime state mutated by readiness confirmation")
    return errors

def attach_readiness_confirmation_metadata_to_paper_analytics(payload: dict[str, Any], review: ReadinessConfirmationReview) -> dict[str, Any]:
    res = payload.copy()
    res["readiness_confirmation_review_id"] = review.review_id
    return res

def paper_runtime_readiness_confirmation_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Paper snapshot generated"
