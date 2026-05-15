from usa_signal_bot.regime_map.regime_cost_adapter import adjust_regime_cost_decision_with_transition_risk

def test_adjust_cost():
    res = {"decision": "NORMAL"}
    out = adjust_regime_cost_decision_with_transition_risk(res, [])
    assert out == res
