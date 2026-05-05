import datetime
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    NotificationChannel,
    NotificationType,
    NotificationPriority,
    NotificationStatus,
    NotificationDispatchStatus,
    TelegramParseMode,
    NotificationSuppressionReason,
)

@dataclass
class NotificationConfig:
    enabled: bool
    default_channel: NotificationChannel
    dry_run: bool
    log_only: bool
    max_message_length: int
    max_queue_size: int
    suppress_duplicates: bool
    duplicate_window_seconds: int
    rate_limit_per_minute: int
    include_disclaimer: bool
    disclaimer_text: str

@dataclass
class NotificationMessage:
    message_id: str
    notification_type: NotificationType
    channel: NotificationChannel
    priority: NotificationPriority
    title: str
    body: str
    created_at_utc: str
    parse_mode: TelegramParseMode = TelegramParseMode.NONE
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: NotificationStatus = NotificationStatus.CREATED
    suppression_reason: Optional[NotificationSuppressionReason] = None

@dataclass
class QueuedNotification:
    queue_id: str
    message: NotificationMessage
    queued_at_utc: str
    attempts: int = 0
    max_attempts: int = 1
    next_attempt_at_utc: Optional[str] = None

@dataclass
class NotificationDispatchResult:
    dispatch_id: str
    created_at_utc: str
    status: NotificationDispatchStatus
    channel: NotificationChannel
    total_messages: int
    sent_count: int
    failed_count: int
    skipped_count: int
    dry_run_count: int
    suppressed_count: int
    results: List[Dict[str, Any]]
    warnings: List[str]
    errors: List[str]

def notification_config_to_dict(config: NotificationConfig) -> dict:
    return {
        "enabled": config.enabled,
        "default_channel": config.default_channel.value if isinstance(config.default_channel, NotificationChannel) else config.default_channel,
        "dry_run": config.dry_run,
        "log_only": config.log_only,
        "max_message_length": config.max_message_length,
        "max_queue_size": config.max_queue_size,
        "suppress_duplicates": config.suppress_duplicates,
        "duplicate_window_seconds": config.duplicate_window_seconds,
        "rate_limit_per_minute": config.rate_limit_per_minute,
        "include_disclaimer": config.include_disclaimer,
        "disclaimer_text": config.disclaimer_text,
    }

def notification_message_to_dict(message: NotificationMessage) -> dict:
    return {
        "message_id": message.message_id,
        "notification_type": message.notification_type.value if isinstance(message.notification_type, NotificationType) else message.notification_type,
        "channel": message.channel.value if isinstance(message.channel, NotificationChannel) else message.channel,
        "priority": message.priority.value if isinstance(message.priority, NotificationPriority) else message.priority,
        "title": message.title,
        "body": message.body,
        "created_at_utc": message.created_at_utc,
        "parse_mode": message.parse_mode.value if isinstance(message.parse_mode, TelegramParseMode) else message.parse_mode,
        "metadata": message.metadata,
        "status": message.status.value if isinstance(message.status, NotificationStatus) else message.status,
        "suppression_reason": message.suppression_reason.value if message.suppression_reason and isinstance(message.suppression_reason, NotificationSuppressionReason) else message.suppression_reason,
    }

def queued_notification_to_dict(item: QueuedNotification) -> dict:
    return {
        "queue_id": item.queue_id,
        "message": notification_message_to_dict(item.message),
        "queued_at_utc": item.queued_at_utc,
        "attempts": item.attempts,
        "max_attempts": item.max_attempts,
        "next_attempt_at_utc": item.next_attempt_at_utc,
    }

def notification_dispatch_result_to_dict(result: NotificationDispatchResult) -> dict:
    return {
        "dispatch_id": result.dispatch_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value if isinstance(result.status, NotificationDispatchStatus) else result.status,
        "channel": result.channel.value if isinstance(result.channel, NotificationChannel) else result.channel,
        "total_messages": result.total_messages,
        "sent_count": result.sent_count,
        "failed_count": result.failed_count,
        "skipped_count": result.skipped_count,
        "dry_run_count": result.dry_run_count,
        "suppressed_count": result.suppressed_count,
        "results": result.results,
        "warnings": result.warnings,
        "errors": result.errors,
    }

def validate_notification_config(config: NotificationConfig) -> None:
    if not isinstance(config.enabled, bool):
        raise ValueError("enabled must be a bool")
    if not isinstance(config.default_channel, NotificationChannel) and config.default_channel not in [c.value for c in NotificationChannel]:
        raise ValueError("default_channel must be a valid NotificationChannel enum")
    if config.max_message_length <= 0:
        raise ValueError("max_message_length must be positive")
    if config.max_queue_size <= 0:
        raise ValueError("max_queue_size must be positive")
    if config.duplicate_window_seconds <= 0:
        raise ValueError("duplicate_window_seconds must be positive")
    if config.rate_limit_per_minute <= 0:
        raise ValueError("rate_limit_per_minute must be positive")

def validate_notification_message(message: NotificationMessage, config: Optional[NotificationConfig] = None) -> None:
    if not message.message_id:
        raise ValueError("message_id cannot be empty")
    if not message.title and not message.body:
        raise ValueError("title or body must be provided")
    if not isinstance(message.channel, NotificationChannel) and message.channel not in [c.value for c in NotificationChannel]:
        raise ValueError("channel must be a valid NotificationChannel enum")
    if not isinstance(message.notification_type, NotificationType) and message.notification_type not in [t.value for t in NotificationType]:
        raise ValueError("notification_type must be a valid NotificationType enum")

def create_notification_message_id(prefix: str = "msg") -> str:
    return f"{prefix}_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

def create_notification_queue_id(prefix: str = "queue") -> str:
    return f"{prefix}_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

def create_notification_dispatch_id(prefix: str = "dispatch") -> str:
    return f"{prefix}_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
