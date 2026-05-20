from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    BridgeTelemetryEvent,
    BridgeTelemetryEventType,
    create_bridge_telemetry_event_id,
    DryRunBridgeSafetyFlag
)

def bridge_operation_allowed(operation: str) -> bool:
    denied = [
        "write_paper_state",
        "send_paper_order",
        "send_broker_order",
        "send_telegram_real",
        "write_production_config",
        "enable_active_paper",
        "mutate_paper_store"
    ]
    return operation not in denied

def monitor_bridge_operation(operation: str, session_id: Optional[str] = None, ref_id: Optional[str] = None) -> BridgeTelemetryEvent:
    if bridge_operation_allowed(operation):
        return monitor_allowed_operation(operation, session_id)
    else:
        return monitor_denied_operation(operation, session_id)

def monitor_allowed_operation(operation: str, session_id: Optional[str] = None) -> BridgeTelemetryEvent:
    return BridgeTelemetryEvent(
        event_id=create_bridge_telemetry_event_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        event_type=BridgeTelemetryEventType.OUTPUT_WRITTEN,
        session_id=session_id,
        ref_id=operation,
        payload_summary={"operation": operation, "status": "allowed"},
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def monitor_denied_operation(operation: str, session_id: Optional[str] = None) -> BridgeTelemetryEvent:
    flags = []
    if "broker" in operation:
        flags.append(DryRunBridgeSafetyFlag.BROKER_ORDER_RISK)
    if "telegram" in operation:
        flags.append(DryRunBridgeSafetyFlag.TELEGRAM_REAL_SEND_RISK)
    if "config" in operation:
        flags.append(DryRunBridgeSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if "paper" in operation and "write" in operation or "mutate" in operation:
        flags.append(DryRunBridgeSafetyFlag.PAPER_STATE_MUTATION_RISK)
    if "paper" in operation and "send" in operation:
        flags.append(DryRunBridgeSafetyFlag.PAPER_ORDER_RISK)

    if not flags:
        flags.append(DryRunBridgeSafetyFlag.UNKNOWN)

    return BridgeTelemetryEvent(
        event_id=create_bridge_telemetry_event_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        event_type=BridgeTelemetryEventType.BLOCKED_OPERATION_ATTEMPTED,
        session_id=session_id,
        ref_id=operation,
        payload_summary={"operation": operation, "status": "blocked"},
        safety_flags=flags,
        warnings=["Operation denied by bridge operation monitor."],
        errors=[f"Blocked dangerous operation: {operation}"]
    )

def operation_monitor_summary(events: List[BridgeTelemetryEvent]) -> dict[str, Any]:
    return {
        "total_events": len(events),
        "blocked": len([e for e in events if e.event_type == BridgeTelemetryEventType.BLOCKED_OPERATION_ATTEMPTED]),
        "allowed": len([e for e in events if e.event_type != BridgeTelemetryEventType.BLOCKED_OPERATION_ATTEMPTED])
    }

def operation_monitor_to_text(payload: dict[str, Any]) -> str:
    return f"Monitor: {payload.get('allowed', 0)} allowed, {payload.get('blocked', 0)} blocked."
