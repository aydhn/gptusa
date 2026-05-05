import datetime
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class NotificationRateLimitState:
    window_start_utc: str
    sent_in_window: int
    rate_limit_per_minute: int

class NotificationRateLimiter:
    def __init__(self, rate_limit_per_minute: int = 20):
        self.rate_limit_per_minute = rate_limit_per_minute
        self.window_start: Optional[datetime.datetime] = None
        self.sent_count = 0

    def allow(self, now_utc: Optional[str] = None) -> Tuple[bool, str]:
        now = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)

        if not self.window_start:
            self.window_start = now
            self.sent_count = 0

        elapsed = (now - self.window_start).total_seconds()

        # Reset window if more than 60 seconds passed
        if elapsed >= 60.0:
            self.window_start = now
            self.sent_count = 0

        if self.sent_count >= self.rate_limit_per_minute:
            return False, f"Rate limit reached ({self.rate_limit_per_minute} msgs/min)"

        return True, "Allowed"

    def record_send(self, now_utc: Optional[str] = None) -> None:
        now = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)

        if not self.window_start:
            self.window_start = now
            self.sent_count = 0

        elapsed = (now - self.window_start).total_seconds()
        if elapsed >= 60.0:
            self.window_start = now
            self.sent_count = 0

        self.sent_count += 1

    def reset(self, now_utc: Optional[str] = None) -> None:
        now = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)
        self.window_start = now
        self.sent_count = 0

    def state(self) -> NotificationRateLimitState:
        return NotificationRateLimitState(
            window_start_utc=self.window_start.isoformat() if self.window_start else "",
            sent_in_window=self.sent_count,
            rate_limit_per_minute=self.rate_limit_per_minute
        )

def notification_rate_limit_state_to_dict(state: NotificationRateLimitState) -> dict:
    return {
        "window_start_utc": state.window_start_utc,
        "sent_in_window": state.sent_in_window,
        "rate_limit_per_minute": state.rate_limit_per_minute,
    }
