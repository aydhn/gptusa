from typing import Any
from usa_signal_bot.paper_controlled_planning.planning_models import (
    PaperAdjacentRehearsalContext,
    PaperAdjacentRehearsalRun,
    ControlledPlanningReview
)
from usa_signal_bot.paper_controlled_planning.adjacent_rehearsal_context import build_mock_paper_adjacent_rehearsal_context
from usa_signal_bot.paper_controlled_planning.guarded_rehearsal_runner import GuardedPaperAdjacentRehearsalRunner

def adjacent_rehearsal_context_from_dry_run_review(payload: dict[str, Any]) -> PaperAdjacentRehearsalContext:
    # Converts a dry run review into a paper-adjacent rehearsal context
    context = build_mock_paper_adjacent_rehearsal_context()
    context.candidate_id = payload.get("candidate_id", context.candidate_id)
    return context

def adjacent_rehearsal_run_from_dry_run_review(payload: dict[str, Any]) -> PaperAdjacentRehearsalRun:
    context = adjacent_rehearsal_context_from_dry_run_review(payload)
    runner = GuardedPaperAdjacentRehearsalRunner()
    return runner.run_rehearsal(context)

def attach_planning_hint_to_dry_run_payload(payload: dict[str, Any], review: ControlledPlanningReview) -> dict[str, Any]:
    payload["controlled_planning_hint"] = "Consider generating a controlled planning ticket."
    payload["planning_review_id"] = review.review_id
    return payload

def dry_run_bridge_planning_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": payload.get("candidate_id"),
        "has_planning_hint": "controlled_planning_hint" in payload
    }

def dry_run_bridge_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = dry_run_bridge_planning_summary(payload)
    lines = [
        "🔄 DRY-RUN BRIDGE TO CONTROLLED PLANNING ADAPTER",
        f"Candidate ID: {summary['candidate_id'] or 'Unknown'}",
        f"Has Planning Hint: {summary['has_planning_hint']}"
    ]
    return "\n".join(lines)
