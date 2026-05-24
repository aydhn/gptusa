import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.final_handoff_freeze_gate import build_default_final_handoff_freeze_gate

def test_build_default_final_handoff_freeze_gate():
    gate = build_default_final_handoff_freeze_gate("cand-1")
    assert gate.candidate_id == "cand-1"
    assert gate.activation_allowed is False
    assert gate.activation_denied is True
    assert gate.order_created is False
    assert gate.frozen is True
    assert gate.sealed is True
