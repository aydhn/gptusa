import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_gate_adapter import simulator_gate_supports_handoff_freeze

def test_simulator_gate_supports_handoff_freeze():
    payload = {"simulator_admission_allowed": True}
    valid, warnings = simulator_gate_supports_handoff_freeze(payload)
    assert valid is False
    assert len(warnings) > 0
