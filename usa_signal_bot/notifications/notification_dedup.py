import datetime
import hashlib
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Any

from usa_signal_bot.notifications.notification_models import NotificationMessage, NotificationSuppressionReason

@dataclass
class NotificationDedupRecord:
    dedup_key: str
    message_id: str
    created_at_utc: str
    expires_at_utc: Optional[str]

class NotificationDeduplicator:
    def __init__(self, window_seconds: int = 3600):
        self.window_seconds = window_seconds
        self._records: Dict[str, NotificationDedupRecord] = {}

    def dedup_key_for_message(self, message: NotificationMessage) -> str:
        # Create a deterministic key based on type, title, and body
        raw = f"{message.notification_type.value}_{message.title}_{message.body}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    def should_suppress(self, message: NotificationMessage, now_utc: Optional[str] = None) -> Tuple[bool, Optional[NotificationSuppressionReason]]:
        self.clear_expired(now_utc)

        key = self.dedup_key_for_message(message)
        if key in self._records:
            return True, NotificationSuppressionReason.DUPLICATE

        return False, None

    def remember(self, message: NotificationMessage, now_utc: Optional[str] = None) -> NotificationDedupRecord:
        now = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)
        expires = now + datetime.timedelta(seconds=self.window_seconds)

        key = self.dedup_key_for_message(message)

        record = NotificationDedupRecord(
            dedup_key=key,
            message_id=message.message_id,
            created_at_utc=now.isoformat(),
            expires_at_utc=expires.isoformat()
        )

        self._records[key] = record
        return record

    def clear_expired(self, now_utc: Optional[str] = None) -> int:
        now = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)
        now_str = now.isoformat()

        expired_keys = []
        for key, record in self._records.items():
            if record.expires_at_utc and record.expires_at_utc <= now_str:
                expired_keys.append(key)

        for key in expired_keys:
            del self._records[key]

        return len(expired_keys)

    def list_records(self) -> List[NotificationDedupRecord]:
        return list(self._records.values())

def notification_dedup_record_to_dict(record: NotificationDedupRecord) -> dict:
    return {
        "dedup_key": record.dedup_key,
        "message_id": record.message_id,
        "created_at_utc": record.created_at_utc,
        "expires_at_utc": record.expires_at_utc,
    }
