from usa_signal_bot.notifications.notification_reporting import notification_message_to_text, notification_limitations_text
from usa_signal_bot.notifications.notification_models import NotificationMessage
from usa_signal_bot.core.enums import NotificationChannel, NotificationType, NotificationPriority

def test_notification_message_to_text():
    msg = NotificationMessage(
        message_id="1",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.NORMAL,
        title="T", body="B", created_at_utc="now"
    )
    txt = notification_message_to_text(msg)
    assert "Message ID: 1" in txt
    assert "T" in txt

def test_notification_limitations_text():
    txt = notification_limitations_text()
    assert "investment advice" in txt
