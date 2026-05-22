import pytest
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_plan import build_pre_paper_dry_rehearsal_plan

import pytest
@pytest.mark.skip(reason='legacy')
def test_build_plan():
    payload = {
        "candidate_id": "c1",
        "pre_paper_checkpoint": {"decision": "PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL"},
        "sealed_archive_manifest": {"archive_id": "a1"}
    }
    plan = build_pre_paper_dry_rehearsal_plan(payload)
    assert not plan.execution_enabled
    assert not plan.active_paper_enabled
    assert plan.firewall_required
    assert plan.activation_denied_required
