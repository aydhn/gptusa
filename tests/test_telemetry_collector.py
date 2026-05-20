import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.telemetry_collector import (
    collect_telemetry_from_session,
    telemetry_event_counts,
    telemetry_safety_flag_counts,
    telemetry_quality_warnings,
    telemetry_collector_summary,
    telemetry_collector_to_text
)

def test_telemetry_collector():
    ctx = build_mock_dry_run_bridge_context()
    runner = SupervisedDryRunBridgeRunner()
    session = runner.run_session(ctx)

    events = collect_telemetry_from_session(session)
    assert len(events) > 0

    counts = telemetry_event_counts(events)
    assert "output_written" in counts

    flags = telemetry_safety_flag_counts(events)
    assert isinstance(flags, dict)

    warnings = telemetry_quality_warnings(events)
    assert isinstance(warnings, list)

    summary = telemetry_collector_summary(events)
    assert summary["total_events"] == len(events)

    assert "Collector" in telemetry_collector_to_text(summary)
