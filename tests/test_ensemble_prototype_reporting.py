from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_reporting import ensemble_prototype_limitations_text

def test_ensemble_prototype_limitations_text():
    assert "Offline" in ensemble_prototype_limitations_text()
