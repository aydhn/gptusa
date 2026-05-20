from typing import Any

def collect_operational_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    metrics = {
        "latest_dry_run_bridge_session_count": payload.get("session_count", 0),
        "latest_dry_run_bridge_completed_count": payload.get("completed_count", 0),
        "latest_dry_run_bridge_blocked_count": payload.get("blocked_count", 0),
        "latest_dry_run_proposal_count": payload.get("proposal_count", 0),
        "latest_dry_run_risk_warning_count": payload.get("risk_warning_count", 0),
        "latest_dry_run_blocked_operation_count": payload.get("blocked_operation_count", 0),
        "latest_human_checkpoint_required_count": payload.get("checkpoint_required_count", 0),
        "latest_human_checkpoint_waiting_count": payload.get("checkpoint_waiting_count", 0),
        "latest_dry_run_bridge_safety_flag_count": payload.get("safety_flag_count", 0),
        "dry_run_bridge_warning_count": payload.get("warning_count", 0),
        # Phase 74 Extensions
        "latest_observation_window_count": payload.get("observation_window_count", 0),
        "latest_observation_completed_count": payload.get("observation_completed_count", 0),
        "latest_observation_blocked_count": payload.get("observation_blocked_count", 0),
        "latest_observation_checkpoint_count": payload.get("observation_checkpoint_count", 0),
        "latest_observation_stale_checkpoint_count": payload.get("observation_stale_checkpoint_count", 0),
        "latest_observation_blocked_operation_count": payload.get("observation_blocked_operation_count", 0),
        "latest_quarantine_exit_eligible_planning_count": payload.get("quarantine_exit_eligible_count", 0),
        "latest_quarantine_exit_retest_count": payload.get("quarantine_exit_retest_count", 0),
        "latest_observation_safety_flag_count": payload.get("observation_safety_flag_count", 0),
        "observation_warning_count": payload.get("observation_warning_count", 0)
    }
    return metrics
