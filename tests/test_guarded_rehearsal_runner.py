from usa_signal_bot.paper_controlled_planning.guarded_rehearsal_runner import GuardedPaperAdjacentRehearsalRunner, validate_rehearsal_run_safety
from usa_signal_bot.paper_controlled_planning.adjacent_rehearsal_context import build_mock_paper_adjacent_rehearsal_context
from usa_signal_bot.core.enums import PaperAdjacentRehearsalStatus

def test_rehearsal_runner():
    ctx = build_mock_paper_adjacent_rehearsal_context()
    runner = GuardedPaperAdjacentRehearsalRunner()
    run = runner.run_rehearsal(ctx)
    assert run.status == PaperAdjacentRehearsalStatus.COMPLETED
    assert not validate_rehearsal_run_safety(run)
