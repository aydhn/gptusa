import pytest
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_runner import GuardedPrePaperDryRehearsalRunner
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_plan import build_default_pre_paper_dry_rehearsal_plan
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_report import build_pre_paper_dry_rehearsal_review

def test_report():
    runner = GuardedPrePaperDryRehearsalRunner()
    plan = build_default_pre_paper_dry_rehearsal_plan()
    run = runner.run_rehearsal(plan)
    rev = build_pre_paper_dry_rehearsal_review(run)
    assert len(rev.runs) == 1
