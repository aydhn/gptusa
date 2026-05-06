from usa_signal_bot.notifications.notification_dispatcher import NotificationDispatcher
from usa_signal_bot.notifications.notification_models import NotificationConfig, NotificationMessage
from usa_signal_bot.core.enums import NotificationChannel, NotificationType, NotificationPriority
from usa_signal_bot.notifications.alert_models import AlertEvaluationResult

def test_dispatch_alert_evaluation():
    config = NotificationConfig(enabled=True, default_channel=NotificationChannel.DRY_RUN, dry_run=True, log_only=True, max_message_length=1000, max_queue_size=100, suppress_duplicates=False, duplicate_window_seconds=10, rate_limit_per_minute=10, include_disclaimer=False, disclaimer_text="")
    dispatcher = NotificationDispatcher(config)

    msg = NotificationMessage(
        message_id="m1",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.NORMAL,
        title="Test",
        body="Test Body",
        created_at_utc="now"
    )

    eval_res = AlertEvaluationResult("e1", "now", "r1", 1, 1, 0, 1, 1, [], [msg], [], [])

    dispatch_res = dispatcher.dispatch_alert_evaluation(eval_res)
    assert dispatch_res.total_messages == 1
    assert dispatch_res.dry_run_count == 1
