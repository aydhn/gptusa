import pytest
from usa_signal_bot.paper_pre_rehearsal.rehearsal_output_analyzer import analyze_pre_paper_rehearsal_run
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_runner import GuardedPrePaperDryRehearsalRunner
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_plan import build_default_pre_paper_dry_rehearsal_plan

def test_analyze():
    runner = GuardedPrePaperDryRehearsalRunner()
    plan = build_default_pre_paper_dry_rehearsal_plan()
    run = runner.run_rehearsal(plan)
    res = analyze_pre_paper_rehearsal_run(run)
    assert res["blocked_event_count"] > 0
