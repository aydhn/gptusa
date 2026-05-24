import re
from pathlib import Path

def update_notifications():
    path = Path("usa_signal_bot/notifications/notification_templates.py")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("from dataclasses import dataclass\n@dataclass\nclass NotificationMessage:\n    message_id: str\n    message_type: str\n    subject: str\n    body: str\n    priority: str\n    channels: list\n    metadata: dict\n")

    content = path.read_text()

    if "format_dry_admission_gate_report_message" not in content:
        templates_to_add = """
def format_dry_admission_gate_report_message(review: dict) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType
    passed = review.get("gate_passed", False)
    status = "PASSED" if passed else "FAILED"
    subject = f"Dry Admission Gate Review - {status}"
    body = f"Dry admission gate evaluation completed.\\nStatus: {status}\\nLimitations: No active paper/broker/live/demo allowed.\\nNot investment advice."
    return NotificationMessage(
        message_id="preview",
        message_type=NotificationType.DRY_ADMISSION_GATE_REPORT.value if hasattr(NotificationType, 'DRY_ADMISSION_GATE_REPORT') else "DRY_ADMISSION_GATE_REPORT",
        subject=subject,
        body=body,
        priority="HIGH",
        channels=["dry_run"],
        metadata=review
    )

def format_shadow_launch_replay_warning_message(results: list) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType
    subject = "Shadow Launch Replay Warning"
    body = f"Issues detected in {len(results)} shadow replay attempts."
    return NotificationMessage(
        message_id="preview",
        message_type=NotificationType.SHADOW_LAUNCH_REPLAY_WARNING.value if hasattr(NotificationType, 'SHADOW_LAUNCH_REPLAY_WARNING') else "SHADOW_LAUNCH_REPLAY_WARNING",
        subject=subject,
        body=body,
        priority="HIGH",
        channels=["dry_run"],
        metadata={"count": len(results)}
    )

def format_board_evidence_freeze_warning_message(freezes: list) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType
    subject = "Board Evidence Freeze Warning"
    body = f"Issues detected in {len(freezes)} evidence freezes (missing or stale)."
    return NotificationMessage(
        message_id="preview",
        message_type=NotificationType.BOARD_EVIDENCE_FREEZE_WARNING.value if hasattr(NotificationType, 'BOARD_EVIDENCE_FREEZE_WARNING') else "BOARD_EVIDENCE_FREEZE_WARNING",
        subject=subject,
        body=body,
        priority="HIGH",
        channels=["dry_run"],
        metadata={"count": len(freezes)}
    )

def notifications_from_dry_admission_gate_review(review: dict) -> list['NotificationMessage']:
    messages = []
    messages.append(format_dry_admission_gate_report_message(review))
    return messages
"""
        content += templates_to_add
        path.write_text(content)

update_notifications()
