from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_safety_validator import ensemble_prototype_text_has_trade_or_execution_language

def test_ensemble_prototype_text_has_trade_or_execution_language():
    assert ensemble_prototype_text_has_trade_or_execution_language("This model gives guaranteed profit") is True
    assert ensemble_prototype_text_has_trade_or_execution_language("This is a research prototype score") is False
