import json
from pathlib import Path
from typing import Any, Dict, Optional

from usa_signal_bot.notifications.notification_models import NotificationMessage, NotificationDispatchResult, NotificationConfig
from usa_signal_bot.notifications.telegram_sender import SendResult
from usa_signal_bot.notifications.notification_validation import NotificationValidationReport

def notification_message_to_text(message: NotificationMessage) -> str:
    status_str = message.status.value if hasattr(message.status, "value") else str(message.status)
    channel_str = message.channel.value if hasattr(message.channel, "value") else str(message.channel)
    lines = [
        f"Message ID: {message.message_id}",
        f"Status: {status_str} | Channel: {channel_str}",
        f"Title: {message.title}",
        "---",
        message.body,
        "---"
    ]
    return "\n".join(lines)

def notification_dispatch_result_to_text(result: NotificationDispatchResult) -> str:
    status_str = result.status.value if hasattr(result.status, "value") else str(result.status)
    channel_str = result.channel.value if hasattr(result.channel, "value") else str(result.channel)
    lines = [
        f"Dispatch ID: {result.dispatch_id}",
        f"Created At: {result.created_at_utc}",
        f"Status: {status_str} | Channel: {channel_str}",
        f"Total Messages: {result.total_messages}",
        f"Sent: {result.sent_count} | Failed: {result.failed_count} | Skipped: {result.skipped_count}",
        f"Dry Run: {result.dry_run_count} | Suppressed: {result.suppressed_count}"
    ]
    if result.warnings:
        lines.append(f"Warnings: {len(result.warnings)}")
        for w in result.warnings[:3]:
            lines.append(f"  - {w}")
    if result.errors:
        lines.append(f"Errors: {len(result.errors)}")
        for e in result.errors[:3]:
            lines.append(f"  - {e}")

    return "\n".join(lines)

def send_result_to_text(result: SendResult) -> str:
    status_str = result.status.value if hasattr(result.status, "value") else str(result.status)
    return f"SendResult[{result.message_id}] -> {status_str}"

def notification_config_to_text(config: NotificationConfig) -> str:
    lines = [
        f"Enabled: {config.enabled}",
        f"Default Channel: {config.default_channel}",
        f"Dry Run: {config.dry_run} | Log Only: {config.log_only}",
        f"Rate Limit: {config.rate_limit_per_minute}/min | Suppress Duplicates: {config.suppress_duplicates}"
    ]
    return "\n".join(lines)

def telegram_config_status_to_text(status: Dict[str, Any]) -> str:
    lines = [
        f"Enabled: {status.get('enabled')}",
        f"Dry Run: {status.get('dry_run')}",
        f"Allow Real Send: {status.get('allow_real_send')}",
        f"Token Present: {status.get('token_present')}",
        f"Token Redacted: {status.get('token_redacted')}",
        f"Chat ID Present: {status.get('chat_id_present')}",
    ]
    return "\n".join(lines)

def notification_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Notification Runs: {summary.get('total_runs', 0)} | Latest: {summary.get('latest_run', 'None')}"

def notification_limitations_text() -> str:
    return (
        "*** NOTIFICATION LIMITATIONS ***\n"
        "- Telegram messages are NOT investment advice.\n"
        "- Telegram messages do NOT create live, demo, or paper orders.\n"
        "- Broker routing and live execution is strictly prohibited.\n"
        "- This is a local research and notification system only."
    )

def write_notification_report_json(path: Path, result: NotificationDispatchResult, validation_report: Optional[NotificationValidationReport] = None) -> Path:
    data = {
        "dispatch_id": result.dispatch_id,
        "text": notification_dispatch_result_to_text(result),
        "validation_passed": validation_report.valid if validation_report else None
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path
