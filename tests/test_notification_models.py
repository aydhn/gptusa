import pytest
from usa_signal_bot.core.enums import NotificationChannel, NotificationType, NotificationPriority, NotificationStatus
from usa_signal_bot.notifications.notification_models import (
    NotificationConfig,
    NotificationMessage,
    QueuedNotification,
    validate_notification_config,
    validate_notification_message,
    create_notification_message_id
)

def test_notification_config_valid():
    config = NotificationConfig(
        enabled=True,
        default_channel=NotificationChannel.DRY_RUN,
        dry_run=True,
        log_only=True,
        max_message_length=3500,
        max_queue_size=1000,
        suppress_duplicates=True,
        duplicate_window_seconds=3600,
        rate_limit_per_minute=20,
        include_disclaimer=True,
        disclaimer_text="Test"
    )
    validate_notification_config(config)

def test_notification_config_invalid():
    config = NotificationConfig(
        enabled=True,
        default_channel=NotificationChannel.DRY_RUN,
        dry_run=True,
        log_only=True,
        max_message_length=-1,
        max_queue_size=1000,
        suppress_duplicates=True,
        duplicate_window_seconds=3600,
        rate_limit_per_minute=20,
        include_disclaimer=True,
        disclaimer_text="Test"
    )
    with pytest.raises(ValueError):
        validate_notification_config(config)

def test_notification_message_valid():
    msg = NotificationMessage(
        message_id=create_notification_message_id(),
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.LOG_ONLY,
        priority=NotificationPriority.NORMAL,
        title="Test Title",
        body="Test Body",
        created_at_utc="now"
    )
    validate_notification_message(msg)

def test_notification_message_empty():
    msg = NotificationMessage(
        message_id=create_notification_message_id(),
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.LOG_ONLY,
        priority=NotificationPriority.NORMAL,
        title="",
        body="",
        created_at_utc="now"
    )
    with pytest.raises(ValueError):
        validate_notification_message(msg)
