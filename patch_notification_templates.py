import re

with open("usa_signal_bot/notifications/notification_templates.py", "r") as f:
    content = f.read()

new_funcs = """
def format_runtime_registry_report_message(review: Any) -> NotificationMessage:
    content = f"Runtime Registry Normalized: {review.review_id}\\n"
    content += "Status: " + ("VALIDATED_NON_EXECUTION" if not review.errors else "BLOCKED")
    content += "\\nNote: Phase 102 runtime registry. Not an activation. No live execution."
    return NotificationMessage(content=content)

def notifications_from_runtime_registry_review(review: Any) -> list[NotificationMessage]:
    msgs = [format_runtime_registry_report_message(review)]
    if review.warnings:
        msgs.append(NotificationMessage(content="Warnings detected in runtime registry."))
    return msgs
"""

if "format_runtime_registry_report_message" not in content:
    content = content + "\n" + new_funcs + "\n"
    with open("usa_signal_bot/notifications/notification_templates.py", "w") as f:
        f.write(content)
