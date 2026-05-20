from typing import Any, List, Optional
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    BridgeTelemetryEvent,
    BridgeTelemetryEventType,
    DryRunBridgeSafetyFlag
)
from usa_signal_bot.paper_dry_run_bridge.operation_monitor import monitor_denied_operation

def create_blocked_operation_event(operation: str, reason: str, session_id: Optional[str] = None) -> BridgeTelemetryEvent:
    event = monitor_denied_operation(operation, session_id)
    event.errors.append(f"Reason: {reason}")
    return event

def blocked_operation_events(events: List[BridgeTelemetryEvent]) -> List[BridgeTelemetryEvent]:
    return [e for e in events if e.event_type == BridgeTelemetryEventType.BLOCKED_OPERATION_ATTEMPTED]

def blocked_operation_count(events: List[BridgeTelemetryEvent]) -> int:
    return len(blocked_operation_events(events))

def blocked_operation_safety_flags(operation: str) -> List[DryRunBridgeSafetyFlag]:
    event = monitor_denied_operation(operation)
    return event.safety_flags

def blocked_operation_telemetry_summary(events: List[BridgeTelemetryEvent]) -> dict[str, Any]:
    blocked = blocked_operation_events(events)
    return {
        "count": len(blocked),
        "operations": list(set(e.ref_id for e in blocked if e.ref_id))
    }

def blocked_operation_telemetry_to_text(payload: dict[str, Any]) -> str:
    return f"Blocked Operations: {payload.get('count', 0)}"
