import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.session_registry import (
    register_dry_run_bridge_session,
    find_dry_run_session_by_id,
    find_dry_run_sessions_by_candidate_id,
    latest_dry_run_session_for_candidate,
    dry_run_session_registry_summary,
    dry_run_session_registry_to_text
)

def test_session_registry():
    ctx = build_mock_dry_run_bridge_context()
    runner = SupervisedDryRunBridgeRunner()
    session = runner.run_session(ctx)

    registry = register_dry_run_bridge_session(session)
    assert len(registry) == 1

    found = find_dry_run_session_by_id(registry, session.session_id)
    assert found is not None
    assert found.session_id == session.session_id

    by_cand = find_dry_run_sessions_by_candidate_id(registry, ctx.candidate_id)
    if ctx.candidate_id:
        assert len(by_cand) == 1

    latest = latest_dry_run_session_for_candidate(registry, ctx.candidate_id)
    if ctx.candidate_id:
        assert latest is not None

    summary = dry_run_session_registry_summary(registry)
    assert summary["total_sessions"] == 1

    assert "Session Registry" in dry_run_session_registry_to_text(registry)
