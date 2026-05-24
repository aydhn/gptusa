from dataclasses import dataclass
from typing import Any

@dataclass
class NotificationMessage:
    content: str
    channel: str = "dry_run"

def format_board_dossier_report_message(review: Any) -> NotificationMessage:
    content = f"Board Dossier Report: {review.review_id}\n"
    content += "Status: " + ("VALIDATED_NON_EXECUTION" if not review.errors else "BLOCKED")
    content += "\nNote: Board dossier review required. No actual paper launch or broker execution occurs."
    return NotificationMessage(content=content)

def format_acceptance_board_seal_warning_message(seals: list[Any]) -> NotificationMessage:
    content = f"Acceptance Board Seal Warning: {len(seals)} seals require review."
    return NotificationMessage(content=content)

def format_shadow_launch_blocker_warning_message(events: list[Any]) -> NotificationMessage:
    unblocked = sum(1 for e in events if not e.blocked)
    content = f"Shadow Launch Blocker Warning: {unblocked} attempts were not blocked."
    return NotificationMessage(content=content)

def notifications_from_board_dossier_review(review: Any) -> list[NotificationMessage]:
    msgs = [format_board_dossier_report_message(review)]
    if review.warnings:
        msgs.append(NotificationMessage(content="Warnings detected in board dossier."))
    return msgs
