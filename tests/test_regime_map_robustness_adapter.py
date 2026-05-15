from usa_signal_bot.regime_map.robustness_adapter import adjust_cost_fragility_with_regime_transition

def test_adjust_fragility():
    res = {"fragility_score": 10.0}
    out = adjust_cost_fragility_with_regime_transition(res, [])
    assert out == res
