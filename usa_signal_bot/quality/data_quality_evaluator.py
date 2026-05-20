from typing import Any, List

def calculate_quality_scorecard(payload: dict[str, Any]) -> dict[str, Any]:
    scorecard = {
        "overall_score": 100,
        "dry_run_bridge_quality_score": 100,
        "bridge_telemetry_completeness_score": 100,
        "dry_run_proposal_safety_score": 100,
        "human_checkpoint_quality_score": 100,
        "paper_snapshot_read_only_score": 100,
        # Phase 74 Extensions
        "observation_window_quality_score": 100,
        "checkpoint_history_quality_score": 100,
        "telemetry_history_quality_score": 100,
        "quarantine_exit_safety_score": 100,
        "observation_decision_consistency_score": 100
    }

    if not payload.get("candidate_id"):
        scorecard["dry_run_bridge_quality_score"] -= 10
    if not payload.get("ticket_id"):
        scorecard["dry_run_bridge_quality_score"] -= 10

    if payload.get("checkpoint_required", False):
        if not payload.get("checkpoint_has_notes", False):
            scorecard["human_checkpoint_quality_score"] -= 20

    blocked_count = payload.get("blocked_operation_count", 0)
    if blocked_count > 0:
        scorecard["bridge_telemetry_completeness_score"] = min(100, scorecard["bridge_telemetry_completeness_score"] + 10)
        scorecard["dry_run_proposal_safety_score"] -= (blocked_count * 5)
        scorecard["quarantine_exit_safety_score"] -= (blocked_count * 5)

    if payload.get("missing_sessions_warning"):
        scorecard["observation_window_quality_score"] -= 20

    if payload.get("stale_checkpoint_warning"):
        scorecard["checkpoint_history_quality_score"] -= 20

    for k in scorecard:
        scorecard[k] = max(0, scorecard[k])

    return scorecard
