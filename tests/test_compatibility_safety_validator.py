from usa_signal_bot.regime_classification.alignment.compatibility_safety_validator import alignment_text_has_trade_or_execution_language
def test_safety_validator():
    assert alignment_text_has_trade_or_execution_language("kesin al")
    assert not alignment_text_has_trade_or_execution_language("looks good")
