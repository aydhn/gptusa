from usa_signal_bot.ml_research.ensemble_evaluation.offline_ensemble_evaluation_metrics import calculate_brier_score

def test_calculate_brier_score():
    assert calculate_brier_score([0.9, 0.1], [1, 0]) == 0.1
