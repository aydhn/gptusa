import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_safety_validator import validate_handoff_freeze_safety
from usa_signal_bot.pre_paper_handoff_freeze_gate.final_handoff_freeze_gate import build_default_final_handoff_freeze_gate

def test_validate_handoff_freeze_safety():
    gate = build_default_final_handoff_freeze_gate()
    errors = validate_handoff_freeze_safety(gate=gate)
    assert len(errors) == 0

    gate.active_paper_enabled = True
    errors = validate_handoff_freeze_safety(gate=gate)
    assert len(errors) > 0
    assert any("Blocking safety flags" in e for e in errors)
