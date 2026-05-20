from typing import Any, List

def calculate_quality_scorecard(payload: dict[str, Any]) -> dict[str, Any]:
    scorecard = {
        "overall_score": 100,
        "dry_run_bridge_quality_score": 100,
        "bridge_telemetry_completeness_score": 100,
        "dry_run_proposal_safety_score": 100,
        "human_checkpoint_quality_score": 100,
        "paper_snapshot_read_only_score": 100
    }

    # Missing candidate/ticket decreases score
    if not payload.get("candidate_id"):
        scorecard["dry_run_bridge_quality_score"] -= 10
    if not payload.get("ticket_id"):
        scorecard["dry_run_bridge_quality_score"] -= 10

    # Checkpoints improve security score, but missing notes reduce it
    if payload.get("checkpoint_required", False):
        if not payload.get("checkpoint_has_notes", False):
            scorecard["human_checkpoint_quality_score"] -= 20

    # If telemetry blocked events are present, telemetry score increases, but safety decreases if bad flags are there
    blocked_count = payload.get("blocked_operation_count", 0)
    if blocked_count > 0:
        scorecard["bridge_telemetry_completeness_score"] = min(100, scorecard["bridge_telemetry_completeness_score"] + 10)
        scorecard["dry_run_proposal_safety_score"] -= (blocked_count * 5)

    # Prevent negative scores
    for k in scorecard:
        scorecard[k] = max(0, scorecard[k])

    return scorecard
