from usa_signal_bot.notifications.notification_dispatcher import NotificationDispatcher
from usa_signal_bot.notifications.notification_models import NotificationConfig, NotificationMessage
from usa_signal_bot.core.enums import NotificationChannel, NotificationType, NotificationPriority, NotificationDispatchStatus

def test_dispatcher_dry_run():
    cfg = NotificationConfig(
        enabled=True,
        default_channel=NotificationChannel.DRY_RUN,
        dry_run=True,
        log_only=True,
        max_message_length=3500,
        max_queue_size=10,
        suppress_duplicates=False,
        duplicate_window_seconds=10,
        rate_limit_per_minute=10,
        include_disclaimer=False,
        disclaimer_text=""
    )
    dispatcher = NotificationDispatcher(cfg)

    msg = NotificationMessage(
        message_id="test",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.NORMAL,
        title="T", body="B", created_at_utc="now"
    )

    dispatcher.enqueue(msg)
    res = dispatcher.dispatch_all()

    assert res.status == NotificationDispatchStatus.DRY_RUN_ONLY
    assert res.total_messages == 1
    assert res.dry_run_count == 1
