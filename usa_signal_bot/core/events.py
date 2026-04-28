"""Event system for tracking system operations."""

from dataclasses import dataclass, field
import uuid
from typing import Any, Dict, Optional
from datetime import datetime, timezone

@dataclass
class SystemEvent:
    event_id: str
    event_type: str
    severity: str
    message: str
    component: str
    timestamp_utc: str
    details: Dict[str, Any] = field(default_factory=dict)
    safe_for_telegram: bool = True

def new_event_id() -> str:
    """Generates a new unique event ID."""
    return str(uuid.uuid4())

def create_event(
    event_type: str,
    severity: str,
    message: str,
    component: str,
    details: Optional[Dict[str, Any]] = None,
    safe_for_telegram: bool = True
) -> SystemEvent:
    """Creates a new SystemEvent."""
    valid_severities = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if severity not in valid_severities:
        raise ValueError(f"Invalid severity: {severity}. Must be one of {valid_severities}")

    return SystemEvent(
        event_id=new_event_id(),
        event_type=event_type,
        severity=severity,
        message=message,
        component=component,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        details=details or {},
        safe_for_telegram=safe_for_telegram
    )

def event_to_dict(event: SystemEvent) -> dict:
    """Converts a SystemEvent to a dictionary."""
    return {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "severity": event.severity,
        "message": event.message,
        "component": event.component,
        "timestamp_utc": event.timestamp_utc,
        "details": event.details,
        "safe_for_telegram": event.safe_for_telegram
    }

def validate_event(event: SystemEvent) -> None:
    """Validates a SystemEvent."""
    valid_severities = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if event.severity not in valid_severities:
        raise ValueError(f"Invalid severity: {event.severity}")
    if not event.event_id:
        raise ValueError("Event ID cannot be empty.")
    if not event.event_type:
        raise ValueError("Event type cannot be empty.")
