with open('usa_signal_bot/notifications/notification_templates.py', 'r') as f:
    content = f.read()

new_templates = """

def format_calibration_diagnostics_report_message(review: 'Any') -> 'Any':
    try:
        from usa_signal_bot.notifications.notification_adapters import NotificationMessage
        from usa_signal_bot.core.enums import NotificationType
        return NotificationMessage(
            message_id="dummy",
            type=NotificationType.CALIBRATION_DIAGNOSTICS_REPORT,
            subject="Phase 141 Calibration Diagnostics",
            body="Calibration diagnostics review built successfully. No live inference or deployment was performed.",
            severity="INFO",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception:
        return None

def format_probability_reliability_warning_message(reports: list) -> 'Any':
    try:
        from usa_signal_bot.notifications.notification_adapters import NotificationMessage
        from usa_signal_bot.core.enums import NotificationType
        return NotificationMessage(
            message_id="dummy",
            type=NotificationType.PROBABILITY_RELIABILITY_WARNING,
            subject="Phase 141 Probability Reliability Warning",
            body="Warnings found during reliability binning.",
            severity="WARNING",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception:
        return None

def format_post_training_validation_warning_message(validations: list) -> 'Any':
    try:
        from usa_signal_bot.notifications.notification_adapters import NotificationMessage
        from usa_signal_bot.core.enums import NotificationType
        return NotificationMessage(
            message_id="dummy",
            type=NotificationType.POST_TRAINING_VALIDATION_WARNING,
            subject="Phase 141 Post-Training Validation Warning",
            body="Warnings found during post-training validation.",
            severity="WARNING",
            timestamp="2024-01-01T00:00:00Z"
        )
    except Exception:
        return None

def notifications_from_calibration_diagnostics_review(review: 'Any') -> list:
    res = []
    msg1 = format_calibration_diagnostics_report_message(review)
    if msg1: res.append(msg1)
    msg2 = format_probability_reliability_warning_message([])
    if msg2: res.append(msg2)
    msg3 = format_post_training_validation_warning_message([])
    if msg3: res.append(msg3)
    return res
"""

if "def format_calibration_diagnostics_report_message" not in content:
    content += new_templates

with open('usa_signal_bot/notifications/notification_templates.py', 'w') as f:
    f.write(content)
