from usa_signal_bot.notifications.telegram_config import (
    default_telegram_notification_config,
    validate_telegram_notification_config,
    assert_safe_to_send_telegram,
    redact_telegram_token,
    telegram_config_status
)
from usa_signal_bot.core.enums import TelegramParseMode

def test_default_config_is_safe():
    config = default_telegram_notification_config()
    safe, reasons = assert_safe_to_send_telegram(config)
    assert not safe
    assert "disabled" in reasons[0].lower() or "dry run" in reasons[0].lower()

def test_token_redaction():
    assert redact_telegram_token(None) == "None"
    assert redact_telegram_token("short") == "***"
    assert redact_telegram_token("longertokenstringhere") == "long...here"

def test_validate_telegram_config_valid():
    config = default_telegram_notification_config()
    validate_telegram_notification_config(config)

def test_assert_safe_to_send():
    config = default_telegram_notification_config()
    config.enabled = True
    config.dry_run = False
    config.allow_real_send = True
    # Without env vars it should still be unsafe
    safe, reasons = assert_safe_to_send_telegram(config)
    assert not safe
    assert "missing" in str(reasons).lower()
