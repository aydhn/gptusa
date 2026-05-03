"""Event models for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import BacktestEventType
from usa_signal_bot.core.exceptions import BacktestEventError

@dataclass
class BacktestEvent:
    """A single event in the backtest engine."""
    event_id: str
    event_type: BacktestEventType
    timestamp_utc: str
    symbol: str | None
    timeframe: str | None
    payload: dict[str, Any]
    sequence: int
    created_at_utc: str

@dataclass
class BacktestEventStream:
    """A stream of events in a backtest run."""
    stream_id: str
    events: list[BacktestEvent]
    created_at_utc: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def create_backtest_event(
    event_type: BacktestEventType,
    timestamp_utc: str,
    symbol: str | None,
    timeframe: str | None,
    payload: dict[str, Any],
    sequence: int
) -> BacktestEvent:
    """Create a new BacktestEvent."""
    return BacktestEvent(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        timestamp_utc=timestamp_utc,
        symbol=symbol,
        timeframe=timeframe,
        payload=payload,
        sequence=sequence,
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

def event_to_dict(event: BacktestEvent) -> dict:
    """Convert an event to a dictionary for serialization."""
    return {
        "event_id": event.event_id,
        "event_type": event.event_type.value,
        "timestamp_utc": event.timestamp_utc,
        "symbol": event.symbol,
        "timeframe": event.timeframe,
        "payload": event.payload,
        "sequence": event.sequence,
        "created_at_utc": event.created_at_utc
    }

def event_stream_to_dict(stream: BacktestEventStream) -> dict:
    """Convert an event stream to a dictionary."""
    return {
        "stream_id": stream.stream_id,
        "events": [event_to_dict(e) for e in stream.events],
        "created_at_utc": stream.created_at_utc,
        "warnings": stream.warnings,
        "errors": stream.errors
    }

def sort_events_by_time_sequence(events: list[BacktestEvent]) -> list[BacktestEvent]:
    """Sort events by timestamp_utc and then by sequence."""
    return sorted(events, key=lambda e: (e.timestamp_utc, e.sequence))

def filter_events_by_type(events: list[BacktestEvent], event_type: BacktestEventType) -> list[BacktestEvent]:
    """Filter events by type."""
    return [e for e in events if e.event_type == event_type]

def validate_backtest_event(event: BacktestEvent) -> None:
    """Validate a backtest event.

    Raises:
        BacktestEventError: If the event is invalid.
    """
    if not event.event_id:
        raise BacktestEventError("event_id cannot be empty")
    if not event.timestamp_utc:
        raise BacktestEventError("timestamp_utc cannot be empty")
    if event.sequence < 0:
        raise BacktestEventError("sequence cannot be negative")
    if not isinstance(event.payload, dict):
        raise BacktestEventError("payload must be a dictionary")
