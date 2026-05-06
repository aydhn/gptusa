from usa_signal_bot.notifications.notification_dedup import NotificationDeduplicator
from usa_signal_bot.notifications.notification_models import NotificationMessage
from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority

def test_notification_dedup():
    dedup = NotificationDeduplicator(window_seconds=10)
    msg = NotificationMessage(
        message_id="1",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.LOG_ONLY,
        priority=NotificationPriority.NORMAL,
        title="T", body="B", created_at_utc="now"
    )

    is_dup, reason = dedup.should_suppress(msg)
    assert not is_dup

    dedup.remember(msg)
    is_dup_after, reason_after = dedup.should_suppress(msg)
    assert is_dup_after
    assert reason_after.value == "DUPLICATE"
