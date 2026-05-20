from typing import Any, List
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunBridgeReview, DryRunBridgeSession, HumanReviewCheckpoint
from usa_signal_bot.paper_dry_run_bridge.dry_run_reporting import dry_run_bridge_limitations_text

class NotificationMessage:
    def __init__(self, channel: str, text: str):
        self.channel = channel
        self.text = text

def format_dry_run_bridge_report_message(review: DryRunBridgeReview) -> NotificationMessage:
    lines = [
        "🧪 DRY-RUN BRIDGE REVIEW",
        f"Review ID: {review.review_id}",
        f"Sessions: {len(review.sessions)}",
        f"Total Telemetry Events: {len(review.telemetry_events)}",
        "",
        dry_run_bridge_limitations_text()
    ]
    return NotificationMessage("dry_run", "\n".join(lines))

def format_dry_run_bridge_safety_warning_message(sessions: List[DryRunBridgeSession]) -> NotificationMessage:
    blocked_sessions = [s for s in sessions if s.status == "blocked"]
    lines = [
        "⚠️ DRY-RUN BRIDGE SAFETY WARNING",
        f"Blocked Sessions: {len(blocked_sessions)}",
        "",
        dry_run_bridge_limitations_text()
    ]
    return NotificationMessage("dry_run", "\n".join(lines))

def format_human_review_checkpoint_warning_message(checkpoints: List[HumanReviewCheckpoint]) -> NotificationMessage:
    waiting = [c for c in checkpoints if c.status == "waiting_review"]
    lines = [
        "⚠️ HUMAN REVIEW CHECKPOINT REQUIRED",
        f"Waiting Checkpoints: {len(waiting)}",
        "",
        dry_run_bridge_limitations_text()
    ]
    return NotificationMessage("dry_run", "\n".join(lines))

def notifications_from_dry_run_bridge_review(review: DryRunBridgeReview) -> List[NotificationMessage]:
    return [format_dry_run_bridge_report_message(review)]
