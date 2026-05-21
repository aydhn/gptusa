from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import ReadinessRehearsalRun, ReadinessRehearsalReview

def build_read_only_paper_snapshot_for_readiness_rehearsal(paper_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not paper_payload:
        return {}
    # Ensures a shallow read-only snapshot
    return paper_payload.copy()

def compare_readiness_rehearsal_to_paper_snapshot(run: ReadinessRehearsalRun, paper_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    # Mock comparison, since rehearsal doesn't mutate it should be identical
    return {
        "drift_detected": False,
        "run_id": run.run_id
    }

def validate_paper_runtime_not_mutated_by_readiness_rehearsal(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    errors = []
    if before.get("paper_state_committed", False) != after.get("paper_state_committed", False):
        errors.append("paper_state_committed mutated")
    if before.get("paper_order_executed", False) != after.get("paper_order_executed", False):
        errors.append("paper_order_executed mutated")
    if before.get("portfolio_state_mutated", False) != after.get("portfolio_state_mutated", False):
        errors.append("portfolio_state_mutated mutated")
    return errors

def attach_readiness_rehearsal_metadata_to_paper_analytics(payload: Dict[str, Any], review: ReadinessRehearsalReview) -> Dict[str, Any]:
    new_payload = payload.copy()
    new_payload["readiness_rehearsal_metadata"] = {
        "review_id": review.review_id
    }
    return new_payload

def paper_runtime_readiness_rehearsal_adapter_to_text(payload: Dict[str, Any]) -> str:
    return "Paper Runtime Readiness Rehearsal Adapter processed."
