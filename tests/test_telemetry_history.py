from usa_signal_bot.paper_observation.telemetry_history import (
    aggregate_bridge_telemetry_history, count_telemetry_event_types,
    count_telemetry_safety_flags, telemetry_history_warnings, telemetry_history_to_text
)

def test_telemetry_history():
    events = [
        {"event_type": "PROPOSAL", "session_id": "s1"},
        {"event_type": "BLOCKED_OPERATION", "session_id": "s1", "safety_flags": ["REAL_ORDER_RISK"]}
    ]

    counts = count_telemetry_event_types(events)
    assert counts["PROPOSAL"] == 1

    flags = count_telemetry_safety_flags(events)
    assert flags["REAL_ORDER_RISK"] == 1

    warnings = telemetry_history_warnings(events)
    assert len(warnings) == 1

    summary = aggregate_bridge_telemetry_history(events)
    assert summary.event_count == 2
    assert summary.blocked_operation_count == 1

    text = telemetry_history_to_text(summary)
    assert "Events: 2" in text
