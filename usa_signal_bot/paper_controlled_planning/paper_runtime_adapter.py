from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    PaperAdjacentRehearsalRun,
    ControlledPlanningReview
)
from usa_signal_bot.paper_controlled_planning.paper_snapshot_comparator import (
    build_read_only_paper_snapshot_for_planning,
    validate_paper_snapshot_not_mutated
)

def build_read_only_paper_runtime_snapshot_for_planning(paper_payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return build_read_only_paper_snapshot_for_planning(paper_payload)

def compare_adjacent_rehearsal_to_paper_snapshot(run: PaperAdjacentRehearsalRun, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": run.run_id,
        "is_read_only": paper_snapshot.get("read_only", False),
        "proposals_count": len(run.proposals)
    }

def validate_paper_runtime_not_mutated_by_planning(before: dict[str, Any], after: dict[str, Any]) -> List[str]:
    return validate_paper_snapshot_not_mutated(before, after)

def attach_planning_metadata_to_paper_analytics(payload: dict[str, Any], review: ControlledPlanningReview) -> dict[str, Any]:
    payload["planning_review_id"] = review.review_id
    if review.planning_tickets:
        payload["planning_ticket_id"] = review.planning_tickets[0].ticket_id
    return payload

def paper_runtime_planning_adapter_to_text(payload: dict[str, Any]) -> str:
    lines = [
        "🔄 PAPER RUNTIME ADAPTER",
        "LIMITATION: This adapter creates strict read-only snapshots and NEVER mutates the real paper state."
    ]
    return "\n".join(lines)
