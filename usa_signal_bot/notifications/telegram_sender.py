import json
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import NotificationChannel, NotificationStatus, TelegramParseMode
from usa_signal_bot.notifications.notification_models import NotificationMessage, NotificationConfig
from usa_signal_bot.notifications.telegram_config import (
    TelegramNotificationConfig,
    get_telegram_bot_token,
    get_telegram_chat_id,
    assert_safe_to_send_telegram
)

@dataclass
class SendResult:
    message_id: str
    channel: NotificationChannel
    status: NotificationStatus
    provider_message_id: Optional[str] = None
    response_summary: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def send_result_to_dict(result: SendResult) -> dict:
    return {
        "message_id": result.message_id,
        "channel": result.channel.value if isinstance(result.channel, NotificationChannel) else result.channel,
        "status": result.status.value if isinstance(result.status, NotificationStatus) else result.status,
        "provider_message_id": result.provider_message_id,
        "response_summary": result.response_summary,
        "warnings": result.warnings,
        "errors": result.errors,
    }

class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: NotificationMessage) -> SendResult:
        pass

class LogOnlyNotificationSender(NotificationSender):
    def send(self, message: NotificationMessage) -> SendResult:
        return SendResult(
            message_id=message.message_id,
            channel=NotificationChannel.LOG_ONLY,
            status=NotificationStatus.SENT,
            response_summary={"action": "logged", "title": message.title, "length": len(message.body)}
        )

class DryRunNotificationSender(NotificationSender):
    def send(self, message: NotificationMessage) -> SendResult:
        return SendResult(
            message_id=message.message_id,
            channel=NotificationChannel.DRY_RUN,
            status=NotificationStatus.DRY_RUN,
            response_summary={"action": "dry_run", "title": message.title}
        )

class TelegramNotificationSender(NotificationSender):
    def __init__(self, config: TelegramNotificationConfig):
        self.config = config

    def send(self, message: NotificationMessage) -> SendResult:
        res = SendResult(
            message_id=message.message_id,
            channel=NotificationChannel.TELEGRAM,
            status=NotificationStatus.CREATED
        )

        safe, reasons = assert_safe_to_send_telegram(self.config)
        if not safe:
            if self.config.dry_run:
                res.status = NotificationStatus.DRY_RUN
            else:
                res.status = NotificationStatus.SKIPPED
            res.warnings.extend(reasons)
            res.response_summary["reason"] = "unsafe_config"
            return res

        token = get_telegram_bot_token(self.config)
        chat_id = get_telegram_chat_id(self.config)

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        text = f"*{message.title}*\n\n{message.body}"

        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": self.config.disable_web_page_preview
        }

        if message.parse_mode != TelegramParseMode.NONE:
            payload["parse_mode"] = message.parse_mode.value if isinstance(message.parse_mode, TelegramParseMode) else message.parse_mode

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout_seconds) as response:
                response_data = json.loads(response.read().decode("utf-8"))
                res.status = NotificationStatus.SENT
                res.provider_message_id = str(response_data.get("result", {}).get("message_id", ""))
                res.response_summary["ok"] = response_data.get("ok", False)
                return res
        except urllib.error.HTTPError as e:
            res.status = NotificationStatus.FAILED
            try:
                err_data = json.loads(e.read().decode("utf-8"))
                # Important: Never log the token back out even in errors
                res.errors.append(f"HTTP {e.code}: {err_data.get('description', 'Unknown error')}")
            except Exception:
                res.errors.append(f"HTTP {e.code}: {e.reason}")
            return res
        except Exception as e:
            res.status = NotificationStatus.FAILED
            res.errors.append(str(e))
            return res

def create_sender_for_channel(channel: NotificationChannel, notification_config: NotificationConfig, telegram_config: Optional[TelegramNotificationConfig] = None) -> NotificationSender:
    if not notification_config.enabled:
        return DryRunNotificationSender()

    if channel == NotificationChannel.DRY_RUN or notification_config.dry_run:
        return DryRunNotificationSender()

    if channel == NotificationChannel.LOG_ONLY or notification_config.log_only:
        return LogOnlyNotificationSender()

    if channel == NotificationChannel.TELEGRAM:
        if not telegram_config:
            raise ValueError("Telegram config is required for TELEGRAM channel")
        return TelegramNotificationSender(telegram_config)

    # Default fallback
    return LogOnlyNotificationSender()
