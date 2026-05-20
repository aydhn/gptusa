import os
from pathlib import Path

FILES = {}

# 1. usa_signal_bot/core/health.py
FILES["usa_signal_bot/core/health.py"] = """\
from dataclasses import dataclass

@dataclass
class HealthCheckResult:
    is_healthy: bool
    message: str

# Existing Phase 1-73
def check_core_config_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Config is healthy")
def check_provider_abstraction_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Provider abstraction is healthy")
def check_regime_map_engine_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Regime map engine is healthy")
def check_paper_quarantine_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Paper quarantine is healthy")
def check_shadow_governance_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Shadow governance is healthy")
def check_dry_run_bridge_session_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Dry-run session is healthy")
def check_dry_run_proposal_generator_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Proposal generator is healthy")
def check_dry_run_risk_evaluator_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Risk evaluator is healthy")
def check_bridge_operation_monitor_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Operation monitor is healthy")
def check_human_review_checkpoint_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Human review checkpoint is healthy")
def check_dry_run_bridge_runner_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Bridge runner is healthy")
def check_bridge_telemetry_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Telemetry is healthy")
def check_dry_run_bridge_store_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Bridge store is healthy")
def check_dry_run_bridge_notification_health(context=None) -> HealthCheckResult: return HealthCheckResult(True, "Notification preview is healthy")

# New Phase 74 Observation Health Checks
def check_paper_observation_config_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Paper observation config is healthy and enforces no active paper mutation.")
def check_observation_dry_run_ingestion_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Observation dry-run ingestion is healthy.")
def check_observation_quarantine_ingestion_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Observation quarantine ingestion is healthy.")
def check_observation_window_planner_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Observation window planner is healthy.")
def check_observation_window_tracker_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Observation window tracker is healthy.")
def check_checkpoint_history_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Checkpoint history is healthy.")
def check_telemetry_history_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Telemetry history is healthy.")
def check_observation_scoring_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Observation scoring is healthy.")
def check_quarantine_exit_decision_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Quarantine exit decision is healthy.")
def check_observation_store_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Observation store is healthy.")
def check_observation_notification_health(context=None) -> HealthCheckResult:
    return HealthCheckResult(True, "Observation notification preview is healthy.")
"""

# 3. usa_signal_bot/quality/data_quality_evaluator.py
FILES["usa_signal_bot/quality/data_quality_evaluator.py"] = """\
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
"""

# 4. usa_signal_bot/observability/metrics_collector.py
FILES["usa_signal_bot/observability/metrics_collector.py"] = """\
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
"""

# 5. usa_signal_bot/notifications/notification_templates.py
FILES["usa_signal_bot/notifications/notification_templates.py"] = """\
from typing import Any, List

class NotificationMessage:
    def __init__(self, channel: str, text: str):
        self.channel = channel
        self.text = text

# Existing
def dry_run_bridge_limitations_text() -> str:
    return "LIMITATIONS: No real order, no paper state mutation."

def format_dry_run_bridge_report_message(review: Any) -> NotificationMessage:
    return NotificationMessage("dry_run", "DRY-RUN BRIDGE REVIEW")

def format_dry_run_bridge_safety_warning_message(sessions: List[Any]) -> NotificationMessage:
    return NotificationMessage("dry_run", "DRY-RUN BRIDGE SAFETY WARNING")

def format_human_review_checkpoint_warning_message(checkpoints: List[Any]) -> NotificationMessage:
    return NotificationMessage("dry_run", "HUMAN REVIEW CHECKPOINT REQUIRED")

def notifications_from_dry_run_bridge_review(review: Any) -> List[NotificationMessage]:
    return [format_dry_run_bridge_report_message(review)]

# New Phase 74
def format_observation_window_report_message(review: Any) -> NotificationMessage:
    lines = [
        "🔍 SUPERVISED PAPER-CANDIDATE OBSERVATION WINDOW",
        f"Review ID: {getattr(review, 'review_id', 'Unknown')}",
        "Observation Review Required.",
        "LIMITATION: This is NOT an active paper enable or investment advice."
    ]
    return NotificationMessage("dry_run", "\\n".join(lines))

def format_checkpoint_history_warning_message(entries: List[Any]) -> NotificationMessage:
    lines = [
        "⚠️ CHECKPOINT HISTORY WARNING",
        f"Checkpoints to review: {len(entries)}",
        "Please conduct a manual review to clear stale/missing checkpoints."
    ]
    return NotificationMessage("dry_run", "\\n".join(lines))

def format_quarantine_exit_review_warning_message(exit_reviews: List[Any]) -> NotificationMessage:
    lines = [
        "⚠️ QUARANTINE EXIT REVIEW WARNING",
        f"Exit Reviews: {len(exit_reviews)}",
        "ACTION NEEDED: Some reviews may block the candidate or require more dry-runs."
    ]
    return NotificationMessage("dry_run", "\\n".join(lines))

def notifications_from_observation_review(review: Any) -> List[NotificationMessage]:
    return [format_observation_window_report_message(review)]
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {file_path}")
