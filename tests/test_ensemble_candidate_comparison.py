from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_candidate_comparison import compare_ensemble_to_candidate_metric

def test_compare_ensemble_to_candidate_metric():
    comparison = compare_ensemble_to_candidate_metric("p1", "c1", "accuracy", 0.8, 0.7, "test")
    assert comparison.delta_value > 0.0
    assert comparison.non_trading_comparison is True
    assert comparison.produces_trade_signal is False
