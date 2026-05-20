import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunBridgeSessionStatus

def test_bridge_session_runner():
    ctx = build_mock_dry_run_bridge_context()
    runner = SupervisedDryRunBridgeRunner()

    session = runner.run_session(ctx)

    assert session.status == DryRunBridgeSessionStatus.COMPLETED
    assert len(session.proposals) > 0
    assert len(session.telemetry_events) > 0
    assert len(session.human_checkpoints) == 1

    for p in session.proposals:
        assert p.is_real_order is False
        assert p.will_mutate_paper_state is False
        assert p.will_send_to_broker is False

    for c in session.human_checkpoints:
        assert c.allows_active_paper is False
        assert c.allows_broker_execution is False
        assert c.allows_config_patch is False
