# notifications/notification_adapters.py integration
from typing import Any, Dict, List
from usa_signal_bot.notifications.notification_templates import NotificationMessage

def format_pre_paper_rehearsal_report_message(review: Any) -> NotificationMessage:
    return NotificationMessage("PRE_PAPER_REHEARSAL_REPORT", "pre-paper rehearsal review required. NOT investment advice.")

def format_mutation_firewall_warning_message(events: List[Any]) -> NotificationMessage:
    return NotificationMessage("MUTATION_FIREWALL_WARNING", f"{len(events)} firewall warnings. NOT investment advice.")

def format_activation_denied_checkpoint_warning_message(checkpoints: List[Any]) -> NotificationMessage:
    return NotificationMessage("ACTIVATION_DENIED_CHECKPOINT_WARNING", f"{len(checkpoints)} activation denied warnings. NOT investment advice.")

def notifications_from_pre_paper_rehearsal_review(review: Any) -> List[NotificationMessage]:
    return [format_pre_paper_rehearsal_report_message(review)]


# --- Phase 92 ---
# Phase 92 Adapters
def format_advanced_transition_report_message(review: Any) -> NotificationMessage:
    content = f"Advanced Transition Report: {getattr(review, 'review_id', 'unknown')}\n"
    content += "This is a dry-run preview. No active paper, no live broker execution. NOT investment advice."
    return NotificationMessage(content=content)

def notifications_from_advanced_transition_review(review: Any) -> List[NotificationMessage]:
    return [format_advanced_transition_report_message(review)]
