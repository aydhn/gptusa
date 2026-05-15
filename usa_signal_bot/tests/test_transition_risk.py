import pytest
from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk, transition_risk_to_text
from usa_signal_bot.core.enums import RegimeTransitionRisk

def test_aggregate_transition_risk_empty():
    assert aggregate_transition_risk([]) == RegimeTransitionRisk.NONE

def test_transition_risk_to_text():
    text = transition_risk_to_text([])
    assert "NONE" in text
