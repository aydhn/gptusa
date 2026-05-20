import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.session_analyzer import (
    analyze_dry_run_bridge_session,
    dry_run_session_metrics,
    dry_run_session_warning_flags,
    dry_run_session_block_flags,
    dry_run_session_success_flags,
    dry_run_session_analyzer_to_text
)

def test_session_analyzer():
    ctx = build_mock_dry_run_bridge_context()
    runner = SupervisedDryRunBridgeRunner()
    session = runner.run_session(ctx)

    analysis = analyze_dry_run_bridge_session(session)

    metrics = analysis["metrics"]
    assert metrics["proposal_count"] > 0

    assert "SESSION_COMPLETED" in analysis["success_flags"]

    assert "Analyzer" in dry_run_session_analyzer_to_text(analysis)
