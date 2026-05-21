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
    return NotificationMessage("dry_run", "\n".join(lines))

def format_checkpoint_history_warning_message(entries: List[Any]) -> NotificationMessage:
    lines = [
        "⚠️ CHECKPOINT HISTORY WARNING",
        f"Checkpoints to review: {len(entries)}",
        "Please conduct a manual review to clear stale/missing checkpoints."
    ]
    return NotificationMessage("dry_run", "\n".join(lines))

def format_quarantine_exit_review_warning_message(exit_reviews: List[Any]) -> NotificationMessage:
    lines = [
        "⚠️ QUARANTINE EXIT REVIEW WARNING",
        f"Exit Reviews: {len(exit_reviews)}",
        "ACTION NEEDED: Some reviews may block the candidate or require more dry-runs."
    ]
    return NotificationMessage("dry_run", "\n".join(lines))

def notifications_from_observation_review(review: Any) -> List[NotificationMessage]:
    return [format_observation_window_report_message(review)]

from typing import Any

def format_observer_governance_report_message(review: Any) -> Any:
    return {"message": f"Observer Governance Review {review.review_id} complete. Non-executing report.", "type": "OBSERVER_GOVERNANCE_REPORT"}

def format_observer_evidence_warning_message(refreshes: list[Any]) -> Any:
    return {"message": f"Observer Evidence Warning: {len(refreshes)} evidence refresh issues.", "type": "OBSERVER_EVIDENCE_WARNING"}

def format_observer_comparison_warning_message(reports: list[Any]) -> Any:
    return {"message": f"Observer Comparison Warning: {len(reports)} issues found.", "type": "OBSERVER_COMPARISON_WARNING"}

def notifications_from_observer_governance_review(review: Any) -> list[Any]:
    return [format_observer_governance_report_message(review)]


def format_promotion_dossier_report_message(review: Any) -> NotificationMessage:
    lines = [
        "📄 PROMOTION DOSSIER REPORT",
        f"Review ID: {getattr(review, 'review_id', 'Unknown')}",
        "LIMITATION: This is NOT an active paper enable or investment advice."
    ]
    return NotificationMessage("dry_run", "\n".join(lines))

def format_final_safety_board_warning_message(board_reviews: List[Any]) -> NotificationMessage:
    return NotificationMessage("dry_run", "FINAL SAFETY BOARD WARNING: Review required.")

def format_readiness_package_warning_message(packages: List[Any]) -> NotificationMessage:
    return NotificationMessage("dry_run", "READINESS PACKAGE WARNING: Review required.")

def notifications_from_promotion_dossier_review(review: Any) -> List[NotificationMessage]:
    return [format_promotion_dossier_report_message(review)]
