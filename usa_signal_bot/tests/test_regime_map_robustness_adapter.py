import pytest
from usa_signal_bot.regime_map.robustness_adapter import adjust_cost_fragility_with_regime_transition

def test_adjust_cost_fragility_with_regime_transition():
    payload = {"recommended_stress_scenarios": []}
    enriched = adjust_cost_fragility_with_regime_transition(payload, [])
    assert enriched == payload
