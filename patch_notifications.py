patch = """
# Phase 125 Notification Templates
def format_final_closure_report_message(review: Any) -> NotificationMessage:
    return NotificationMessage("Final Closure Report", "Ready for Phase 126", "FINAL_CLOSURE_REPORT")

def format_freeze_seal_warning_message(seal: Any) -> NotificationMessage:
    return NotificationMessage("Freeze Seal Warning", "Seal is invalid", "FREEZE_SEAL_WARNING")

def format_phase126_kickoff_warning_message(gate: Any) -> NotificationMessage:
    return NotificationMessage("Phase 126 Kickoff Warning", "Gate failed", "PHASE126_KICKOFF_WARNING")

def notifications_from_final_closure_review(review: Any) -> List[NotificationMessage]:
    return [format_final_closure_report_message(review)]
"""

with open("usa_signal_bot/notifications/notification_templates.py", "a") as f:
    f.write("\n" + patch)
