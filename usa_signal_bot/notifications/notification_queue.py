import datetime
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from usa_signal_bot.notifications.notification_models import (
    NotificationMessage,
    QueuedNotification,
    create_notification_queue_id,
    queued_notification_to_dict,
    NotificationStatus
)

class NotificationQueue:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._items: List[QueuedNotification] = []

    def enqueue(self, message: NotificationMessage, max_attempts: int = 1) -> QueuedNotification:
        if len(self._items) >= self.max_size:
            raise RuntimeError(f"Queue size limit reached ({self.max_size})")

        message.status = NotificationStatus.QUEUED

        q_item = QueuedNotification(
            queue_id=create_notification_queue_id(),
            message=message,
            queued_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            max_attempts=max_attempts
        )
        self._items.append(q_item)
        return q_item

    def enqueue_many(self, messages: List[NotificationMessage], max_attempts: int = 1) -> List[QueuedNotification]:
        results = []
        for msg in messages:
            results.append(self.enqueue(msg, max_attempts))
        return results

    def dequeue(self) -> Optional[QueuedNotification]:
        if not self._items:
            return None
        return self._items.pop(0)

    def peek(self) -> Optional[QueuedNotification]:
        if not self._items:
            return None
        return self._items[0]

    def size(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def clear(self) -> int:
        count = len(self._items)
        self._items.clear()
        return count

    def list_items(self) -> List[QueuedNotification]:
        return list(self._items)

def notification_queue_to_dict(queue: NotificationQueue) -> dict:
    return {
        "max_size": queue.max_size,
        "size": queue.size(),
        "items": [queued_notification_to_dict(item) for item in queue.list_items()]
    }

def queued_notifications_to_jsonl(path: Path, items: List[QueuedNotification]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(queued_notification_to_dict(item)) + "\n")
    return path

def read_queued_notifications_jsonl(path: Path) -> List[Dict[str, Any]]:
    items = []
    if not path.exists():
        return items
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items
