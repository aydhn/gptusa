import pytest
from usa_signal_bot.paper_pre_rehearsal.eligibility_checker import evaluate_pre_paper_rehearsal_eligibility
from usa_signal_bot.core.enums import PrePaperDryRehearsalDecision

def test_eligibility():
    payload = {
        "candidate_id": "c1",
        "pre_paper_checkpoint": {"decision": "PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL"},
        "sealed_archive_manifest": {"archive_id": "a1"}
    }
    decision = evaluate_pre_paper_rehearsal_eligibility(payload)
    assert decision == PrePaperDryRehearsalDecision.RUN_GUARDED_PRE_PAPER_DRY_REHEARSAL
