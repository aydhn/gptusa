import pytest
from usa_signal_bot.ml_research.foundation.ml_foundation_report import build_ml_foundation_context

def test_readiness_gate_passes():
    ctx = build_ml_foundation_context()
    assert ctx.ready_for_phase137 is True
    assert ctx.readiness_gate_passed is True
