from usa_signal_bot.paper_shadow.rehearsal_runner import PaperShadowRehearsalRunner
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def test_rehearsal_runner():
    ctx = build_mock_shadow_simulation_context()
    runner = PaperShadowRehearsalRunner()
    session = runner.run_rehearsal(ctx)
    assert session.status == "COMPLETED"
    assert len(session.signals) == 3
    assert len(session.fills) > 0
    assert len(session.pnl_snapshots) > 0
