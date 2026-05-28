from usa_signal_bot.regime_classification.foundation.regime_foundation_safety_validator import validate_regime_columns_safety, regime_foundation_text_has_trade_or_execution_language

def test_validate_regime_columns_safety():
    assert len(validate_regime_columns_safety(["good_column"])) == 0
    assert len(validate_regime_columns_safety(["good_column", "buy_signal"])) == 1

def test_regime_foundation_text_has_trade_or_execution_language():
    assert regime_foundation_text_has_trade_or_execution_language("This is safe") is False
    assert regime_foundation_text_has_trade_or_execution_language("Buy this immediately") is True
