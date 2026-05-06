import os
from dataclasses import dataclass
from typing import Any, Optional, Tuple

from usa_signal_bot.core.enums import TelegramParseMode

@dataclass
class TelegramNotificationConfig:
    enabled: bool
    dry_run: bool
    bot_token_env_var: str
    chat_id_env_var: str
    parse_mode: TelegramParseMode
    timeout_seconds: int
    disable_web_page_preview: bool
    allow_real_send: bool
    redact_token_in_logs: bool

def default_telegram_notification_config() -> TelegramNotificationConfig:
    return TelegramNotificationConfig(
        enabled=False,
        dry_run=True,
        bot_token_env_var="USA_SIGNAL_BOT_TELEGRAM_TOKEN",
        chat_id_env_var="USA_SIGNAL_BOT_TELEGRAM_CHAT_ID",
        parse_mode=TelegramParseMode.NONE,
        timeout_seconds=10,
        disable_web_page_preview=True,
        allow_real_send=False,
        redact_token_in_logs=True
    )

def validate_telegram_notification_config(config: TelegramNotificationConfig) -> None:
    if not config.bot_token_env_var:
        raise ValueError("bot_token_env_var cannot be empty")
    if not config.chat_id_env_var:
        raise ValueError("chat_id_env_var cannot be empty")
    if config.timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")

def get_telegram_bot_token(config: TelegramNotificationConfig) -> Optional[str]:
    return os.environ.get(config.bot_token_env_var)

def get_telegram_chat_id(config: TelegramNotificationConfig) -> Optional[str]:
    return os.environ.get(config.chat_id_env_var)

def redact_telegram_token(token: Optional[str]) -> str:
    if not token:
        return "None"
    if len(token) <= 8:
        return "***"
    return f"{token[:4]}...{token[-4:]}"

def telegram_config_status(config: TelegramNotificationConfig) -> dict[str, Any]:
    token = get_telegram_bot_token(config)
    chat_id = get_telegram_chat_id(config)

    return {
        "enabled": config.enabled,
        "dry_run": config.dry_run,
        "allow_real_send": config.allow_real_send,
        "token_present": token is not None,
        "token_redacted": redact_telegram_token(token) if config.redact_token_in_logs else "REDACTION_DISABLED",
        "chat_id_present": chat_id is not None,
    }

def assert_safe_to_send_telegram(config: TelegramNotificationConfig) -> Tuple[bool, list[str]]:
    reasons = []

    if not config.enabled:
        reasons.append("Telegram notifications are disabled in config")
        return False, reasons

    if config.dry_run:
        reasons.append("Dry run is enabled")
        return False, reasons

    if not config.allow_real_send:
        reasons.append("allow_real_send is false (safe default)")
        return False, reasons

    token = get_telegram_bot_token(config)
    if not token:
        reasons.append(f"Bot token missing in env var: {config.bot_token_env_var}")

    chat_id = get_telegram_chat_id(config)
    if not chat_id:
        reasons.append(f"Chat ID missing in env var: {config.chat_id_env_var}")

    if reasons:
        return False, reasons

    return True, []
