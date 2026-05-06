import datetime
import uuid
from typing import List, Optional, Tuple

from usa_signal_bot.core.enums import NotificationStatus, NotificationDispatchStatus, NotificationSuppressionReason
from usa_signal_bot.notifications.notification_models import (
    NotificationConfig, NotificationMessage, QueuedNotification, NotificationDispatchResult, create_notification_dispatch_id, create_notification_message_id
)
from usa_signal_bot.notifications.notification_queue import NotificationQueue
from usa_signal_bot.notifications.notification_dedup import NotificationDeduplicator
from usa_signal_bot.notifications.notification_rate_limit import NotificationRateLimiter
from usa_signal_bot.notifications.telegram_config import TelegramNotificationConfig
from usa_signal_bot.notifications.telegram_sender import create_sender_for_channel, SendResult
from usa_signal_bot.notifications.notification_templates import chunk_message_text, append_disclaimer

class NotificationDispatcher:
    def __init__(
        self,
        notification_config: NotificationConfig,
        telegram_config: Optional[TelegramNotificationConfig] = None,
        queue: Optional[NotificationQueue] = None,
        deduplicator: Optional[NotificationDeduplicator] = None,
        rate_limiter: Optional[NotificationRateLimiter] = None
    ):
        self.notification_config = notification_config
        self.telegram_config = telegram_config
        self.queue = queue or NotificationQueue(max_size=notification_config.max_queue_size)

        if notification_config.suppress_duplicates:
            self.deduplicator = deduplicator or NotificationDeduplicator(window_seconds=notification_config.duplicate_window_seconds)
        else:
            self.deduplicator = None

        self.rate_limiter = rate_limiter or NotificationRateLimiter(rate_limit_per_minute=notification_config.rate_limit_per_minute)

    def split_message_if_needed(self, message: NotificationMessage) -> List[NotificationMessage]:
        if len(message.body) <= self.notification_config.max_message_length:
            return [message]

        chunks = chunk_message_text(message.body, max_length=self.notification_config.max_message_length)

        result = []
        for i, chunk in enumerate(chunks):
            new_msg = NotificationMessage(
                message_id=create_notification_message_id(),
                notification_type=message.notification_type,
                channel=message.channel,
                priority=message.priority,
                title=f"{message.title} ({i+1}/{len(chunks)})",
                body=chunk,
                created_at_utc=message.created_at_utc,
                parse_mode=message.parse_mode,
                metadata=message.metadata.copy()
            )
            result.append(new_msg)
        return result

    def enqueue(self, message: NotificationMessage) -> Optional[QueuedNotification]:
        if not self.notification_config.enabled:
            message.status = NotificationStatus.SUPPRESSED
            message.suppression_reason = NotificationSuppressionReason.DISABLED_BY_CONFIG
            return None

        # Append disclaimer before enqueueing if enabled
        message.body = append_disclaimer(message.body, self.notification_config)

        chunks = self.split_message_if_needed(message)
        if len(chunks) == 1:
            return self.queue.enqueue(chunks[0])
        else:
            results = []
            for chunk in chunks:
                results.append(self.queue.enqueue(chunk))
            return results[0] # Return the first chunk's queue item for simplicity or modify API

    def enqueue_many(self, messages: List[NotificationMessage]) -> List[QueuedNotification]:
        results = []
        for msg in messages:
            res = self.enqueue(msg)
            if res:
                results.append(res)
        return results

    def should_skip_message(self, message: NotificationMessage) -> Tuple[bool, Optional[NotificationSuppressionReason], str]:
        if not self.notification_config.enabled:
            return True, NotificationSuppressionReason.DISABLED_BY_CONFIG, "Disabled by config"

        if self.deduplicator:
            is_dup, reason = self.deduplicator.should_suppress(message)
            if is_dup:
                return True, reason, "Duplicate message suppressed"

        allowed, rl_msg = self.rate_limiter.allow()
        if not allowed:
            return True, NotificationSuppressionReason.RATE_LIMITED, rl_msg

        return False, None, "Allowed"

    def mark_suppressed(self, message: NotificationMessage, reason: NotificationSuppressionReason) -> NotificationMessage:
        message.status = NotificationStatus.SUPPRESSED
        message.suppression_reason = reason
        return message

    def dispatch_message(self, message: NotificationMessage) -> SendResult:
        skip, reason, skip_msg = self.should_skip_message(message)

        if skip:
            self.mark_suppressed(message, reason)
            return SendResult(
                message_id=message.message_id,
                channel=message.channel,
                status=NotificationStatus.SUPPRESSED,
                response_summary={"reason": skip_msg},
                warnings=[skip_msg]
            )

        sender = create_sender_for_channel(message.channel, self.notification_config, self.telegram_config)
        res = sender.send(message)

        if res.status == NotificationStatus.SENT:
            self.rate_limiter.record_send()
            if self.deduplicator:
                self.deduplicator.remember(message)

        return res

    def dispatch_all(self) -> NotificationDispatchResult:
        res = NotificationDispatchResult(
            dispatch_id=create_notification_dispatch_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status=NotificationDispatchStatus.COMPLETED,
            channel=self.notification_config.default_channel,
            total_messages=0,
            sent_count=0,
            failed_count=0,
            skipped_count=0,
            dry_run_count=0,
            suppressed_count=0,
            results=[],
            warnings=[],
            errors=[]
        )

        if not self.notification_config.enabled:
            res.status = NotificationDispatchStatus.EMPTY
            res.warnings.append("Notifications disabled by config.")
            return res

        total = self.queue.size()
        if total == 0:
            res.status = NotificationDispatchStatus.EMPTY
            return res

        for _ in range(total):
            item = self.queue.dequeue()
            if not item:
                break

            res.total_messages += 1
            send_res = self.dispatch_message(item.message)

            from usa_signal_bot.notifications.telegram_sender import send_result_to_dict
            res.results.append(send_result_to_dict(send_res))

            if send_res.status == NotificationStatus.SENT:
                res.sent_count += 1
            elif send_res.status == NotificationStatus.DRY_RUN:
                res.dry_run_count += 1
            elif send_res.status == NotificationStatus.SUPPRESSED:
                res.suppressed_count += 1
            elif send_res.status == NotificationStatus.SKIPPED:
                res.skipped_count += 1
            elif send_res.status == NotificationStatus.FAILED:
                res.failed_count += 1

        if res.failed_count == total:
            res.status = NotificationDispatchStatus.FAILED
        elif res.failed_count > 0:
            res.status = NotificationDispatchStatus.PARTIAL_SUCCESS
        elif res.dry_run_count == total:
            res.status = NotificationDispatchStatus.DRY_RUN_ONLY

        return res


    def enqueue_alert_messages(self, messages: List[NotificationMessage]):
        return self.enqueue_many(messages)

    def dispatch_alert_evaluation(self, result: 'AlertEvaluationResult') -> NotificationDispatchResult:
        self.enqueue_alert_messages(result.messages)
        return self.dispatch_all()
