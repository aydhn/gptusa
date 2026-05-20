from typing import Any, List
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeSession,
    BridgeTelemetryEvent,
    BridgeTelemetryEventType,
    DryRunBridgeSafetyFlag
)

def collect_telemetry_from_session(session: DryRunBridgeSession) -> List[BridgeTelemetryEvent]:
    return session.telemetry_events

def telemetry_event_counts(events: List[BridgeTelemetryEvent]) -> dict[str, int]:
    counts = {t.value: 0 for t in BridgeTelemetryEventType}
    for e in events:
        counts[e.event_type.value] += 1
    return counts

def telemetry_safety_flag_counts(events: List[BridgeTelemetryEvent]) -> dict[str, int]:
    counts = {}
    for e in events:
        for f in e.safety_flags:
            counts[f.value] = counts.get(f.value, 0) + 1
    return counts

def telemetry_quality_warnings(events: List[BridgeTelemetryEvent]) -> List[str]:
    warnings = []
    blocked = [e for e in events if e.event_type == BridgeTelemetryEventType.BLOCKED_OPERATION_ATTEMPTED]
    if len(blocked) > 0:
        warnings.append(f"Found {len(blocked)} blocked operation attempts in telemetry.")
    return warnings

def telemetry_collector_summary(events: List[BridgeTelemetryEvent]) -> dict[str, Any]:
    return {
        "total_events": len(events),
        "event_counts": telemetry_event_counts(events),
        "safety_flags": telemetry_safety_flag_counts(events)
    }

def telemetry_collector_to_text(payload: dict[str, Any]) -> str:
    return f"Telemetry Collector: {payload.get('total_events', 0)} events."
