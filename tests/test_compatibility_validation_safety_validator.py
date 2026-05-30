import pytest
from usa_signal_bot.regime_classification.validation.compatibility_validation_safety_validator import context_validation_text_has_trade_or_execution_language

def test_context_validation_text_safety():
    assert context_validation_text_has_trade_or_execution_language("This produces a strong buy signal") is True
    assert context_validation_text_has_trade_or_execution_language("This is a low compatibility context") is False
