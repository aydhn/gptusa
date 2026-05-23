# observability/metrics_collector.py integration
from typing import Any, Dict
def collect_pre_paper_rehearsal_metrics() -> Dict[str, Any]:
    return {
        "latest_pre_paper_rehearsal_run_count": 0,
        "latest_pre_paper_rehearsal_blocked_count": 0,
        "latest_mutation_firewall_event_count": 0,
        "latest_mutation_firewall_blocked_count": 0,
        "latest_activation_denied_checkpoint_count": 0,
        "latest_activation_allowed_violation_count": 0,
        "latest_zero_mutation_violation_count": 0,
        "latest_pre_paper_safety_flag_count": 0,
        "pre_paper_rehearsal_warning_count": 0
    }

def collect_dry_admission_metrics(review_payload: dict) -> dict:
    return {
        "latest_dry_admission_run_count": len(review_payload.get("runs", [])),
        "latest_dry_admission_blocked_count": sum(1 for r in review_payload.get("runs", []) if r.get("status") == "BLOCKED"),
        "latest_dry_admission_write_attempt_count": 0,
        "latest_write_lock_refresh_count": len(review_payload.get("write_lock_refreshes", [])),
        "latest_write_lock_refresh_failed_count": sum(1 for w in review_payload.get("write_lock_refreshes", []) if w.get("status") == "FAILED"),
        "latest_human_approval_ledger_count": len(review_payload.get("human_ledgers", [])),
        "latest_human_ledger_activation_risk_count": sum(1 for l in review_payload.get("human_ledgers", []) if l.get("activation_allowed")),
        "latest_no_write_continuity_failure_count": 0,
        "latest_dry_admission_safety_flag_count": len(review_payload.get("warnings", [])),
        "dry_admission_warning_count": len(review_payload.get("warnings", []))
    }

# paper sandbox bridge metrics added in Phase 89
latest_bridge_dry_run_count = 0
latest_bridge_dry_run_blocked_count = 0
latest_no_order_session_count = 0
latest_no_order_session_blocked_count = 0
latest_bridge_replay_count = 0
latest_bridge_replay_blocked_count = 0
latest_dangerous_route_allowed_count = 0
latest_read_only_route_allowed_count = 0
latest_bridge_safety_flag_count = 0
paper_sandbox_bridge_warning_count = 0
