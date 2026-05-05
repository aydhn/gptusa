import pytest
from usa_signal_bot.notifications.notification_queue import NotificationQueue
from usa_signal_bot.notifications.notification_models import NotificationMessage
from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority

def test_notification_queue_enqueue_dequeue():
    q = NotificationQueue(max_size=5)
    msg = NotificationMessage(
        message_id="1",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.LOG_ONLY,
        priority=NotificationPriority.NORMAL,
        title="T", body="B", created_at_utc="now"
    )

    q.enqueue(msg)
    assert q.size() == 1

    popped = q.dequeue()
    assert popped.message.message_id == "1"
    assert q.size() == 0

def test_notification_queue_max_size():
    q = NotificationQueue(max_size=1)
    msg = NotificationMessage(
        message_id="1",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.LOG_ONLY,
        priority=NotificationPriority.NORMAL,
        title="T", body="B", created_at_utc="now"
    )
    q.enqueue(msg)
    with pytest.raises(RuntimeError):
        q.enqueue(msg)
