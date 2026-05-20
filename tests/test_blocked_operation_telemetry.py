import pytest
from usa_signal_bot.paper_dry_run_bridge.operation_monitor import monitor_bridge_operation
from usa_signal_bot.paper_dry_run_bridge.blocked_operation_telemetry import (
    create_blocked_operation_event,
    blocked_operation_events,
    blocked_operation_count,
    blocked_operation_safety_flags,
    blocked_operation_telemetry_summary,
    blocked_operation_telemetry_to_text
)

def test_blocked_operation_telemetry():
    ev1 = monitor_bridge_operation("read_paper_snapshot")
    ev2 = create_blocked_operation_event("send_telegram_real", "Not allowed in dry run")

    blocked = blocked_operation_events([ev1, ev2])
    assert len(blocked) == 1
    assert blocked[0].ref_id == "send_telegram_real"

    assert blocked_operation_count([ev1, ev2]) == 1

    flags = blocked_operation_safety_flags("write_production_config")
    assert len(flags) > 0

    summary = blocked_operation_telemetry_summary([ev1, ev2])
    assert summary["count"] == 1

    assert "Blocked Operations: 1" in blocked_operation_telemetry_to_text(summary)
