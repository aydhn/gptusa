from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_boundary import build_ensemble_prototype_boundary_rules, build_ensemble_prototype_boundary_result

def test_build_ensemble_prototype_boundary_result():
    rules = build_ensemble_prototype_boundary_rules()
    result = build_ensemble_prototype_boundary_result(rules)
    assert result.boundary_passed is True
    assert result.no_live_inference is True
    assert result.no_trade_signal_output is True
    assert result.no_order_decision_output is True
