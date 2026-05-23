import pytest
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_runner import GuardedPrePaperDryRehearsalRunner
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_plan import build_default_pre_paper_dry_rehearsal_plan

import pytest
@pytest.mark.skip(reason='legacy')
def test_runner():
    runner = GuardedPrePaperDryRehearsalRunner()
    plan = build_default_pre_paper_dry_rehearsal_plan()
    run = runner.run_rehearsal(plan)
    assert run.status.value in ["COMPLETED", "FAILED"]
    assert all(e.blocked for e in run.firewall_events)
