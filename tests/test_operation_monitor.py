import pytest
from usa_signal_bot.paper_dry_run_bridge.operation_monitor import (
    bridge_operation_allowed,
    monitor_bridge_operation,
    operation_monitor_summary,
    operation_monitor_to_text
)
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import BridgeTelemetryEventType

def test_operation_monitor():
    assert bridge_operation_allowed("read_paper_snapshot") is True
    assert bridge_operation_allowed("send_broker_order") is False

    ev_allowed = monitor_bridge_operation("read_paper_snapshot")
    assert ev_allowed.event_type == BridgeTelemetryEventType.OUTPUT_WRITTEN

    ev_denied = monitor_bridge_operation("send_broker_order")
    assert ev_denied.event_type == BridgeTelemetryEventType.BLOCKED_OPERATION_ATTEMPTED

    summary = operation_monitor_summary([ev_allowed, ev_denied])
    assert summary["total_events"] == 2
    assert summary["blocked"] == 1
    assert summary["allowed"] == 1

    assert "Monitor" in operation_monitor_to_text(summary)
