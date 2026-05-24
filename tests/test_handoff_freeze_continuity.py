import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_continuity import validate_handoff_freeze_continuity
from usa_signal_bot.pre_paper_handoff_freeze_gate.final_handoff_freeze_gate import build_default_final_handoff_freeze_gate

def test_validate_handoff_freeze_continuity():
    gate = build_default_final_handoff_freeze_gate()
    errors = validate_handoff_freeze_continuity(gate=gate)
    assert len(errors) == 0

    gate.activation_allowed = True
    errors = validate_handoff_freeze_continuity(gate=gate)
    assert len(errors) > 0
    assert any("activation_allowed" in e for e in errors)
