from usa_signal_bot.notifications.notification_validation import validate_no_execution_language, validate_no_sensitive_token_leak
from usa_signal_bot.notifications.notification_models import NotificationMessage
from usa_signal_bot.core.enums import NotificationChannel, NotificationType, NotificationPriority

def test_validate_no_execution_language():
    msg = NotificationMessage(
        message_id="1",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.NORMAL,
        title="Alert", body="You should kesin al this stock now!", created_at_utc="now"
    )
    report = validate_no_execution_language(msg)
    assert not report.valid
    assert len(report.issues) > 0

def test_validate_no_sensitive_token_leak():
    report = validate_no_sensitive_token_leak("Here is the secret: 1234567890:ABCdefGHIjklMNO", "1234567890:ABCdefGHIjklMNO")
    assert not report.valid

    report2 = validate_no_sensitive_token_leak("Normal text", "1234567890:ABCdefGHIjklMNO")
    assert report2.valid
