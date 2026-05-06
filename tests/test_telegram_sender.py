from usa_signal_bot.notifications.telegram_sender import LogOnlyNotificationSender, DryRunNotificationSender, TelegramNotificationSender
from usa_signal_bot.notifications.telegram_config import default_telegram_notification_config
from usa_signal_bot.notifications.notification_models import NotificationMessage
from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority, NotificationStatus

def get_test_msg():
    return NotificationMessage(
        message_id="test",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.LOG_ONLY,
        priority=NotificationPriority.NORMAL,
        title="T", body="B", created_at_utc="now"
    )

def test_log_only_sender():
    sender = LogOnlyNotificationSender()
    res = sender.send(get_test_msg())
    assert res.status == NotificationStatus.SENT
    assert res.channel == NotificationChannel.LOG_ONLY

def test_dry_run_sender():
    sender = DryRunNotificationSender()
    res = sender.send(get_test_msg())
    assert res.status == NotificationStatus.DRY_RUN
    assert res.channel == NotificationChannel.DRY_RUN

def test_telegram_sender_safe_default():
    config = default_telegram_notification_config()
    sender = TelegramNotificationSender(config)
    res = sender.send(get_test_msg())
    assert res.status in [NotificationStatus.DRY_RUN, NotificationStatus.SKIPPED]
