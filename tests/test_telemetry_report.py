import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.telemetry_report import (
    build_bridge_telemetry_report,
    bridge_telemetry_report_summary,
    bridge_telemetry_limitations_text,
    bridge_telemetry_report_to_text
)

def test_telemetry_report():
    ctx = build_mock_dry_run_bridge_context()
    runner = SupervisedDryRunBridgeRunner()
    session = runner.run_session(ctx)

    report = build_bridge_telemetry_report(session)
    assert report["local_only_telemetry"] is True

    summary = bridge_telemetry_report_summary(report)
    assert summary["session_id"] == session.session_id

    assert "NOT external telemetry" in bridge_telemetry_limitations_text()
    assert "Telemetry Report for" in bridge_telemetry_report_to_text(report)
