import pytest
from usa_signal_bot.paper_pre_rehearsal.final_handoff_adapter import final_handoff_pre_paper_summary

def test_adapter():
    payload = {"guarded_pre_paper_rehearsal_review_id": "r1"}
    summary = final_handoff_pre_paper_summary(payload)
    assert summary["has_review"]
