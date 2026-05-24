import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_report import build_handoff_freeze_review_from_parts
from usa_signal_bot.pre_paper_handoff_freeze_gate.final_handoff_freeze_gate import build_default_final_handoff_freeze_gate
from usa_signal_bot.core.enums import PrePaperHandoffFreezeReportType

def test_build_handoff_freeze_review():
    gate = build_default_final_handoff_freeze_gate()
    review = build_handoff_freeze_review_from_parts(gate)
    assert review.report_type == PrePaperHandoffFreezeReportType.FULL_PRE_PAPER_HANDOFF_FREEZE_REVIEW
    assert len(review.gates) == 1
