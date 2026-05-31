from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_safety_validator import (
    research_freeze_text_has_trade_or_execution_language
)

def test_research_freeze_text_has_trade_or_execution_language():
    assert research_freeze_text_has_trade_or_execution_language("This is safe text") is False
    assert research_freeze_text_has_trade_or_execution_language("this is a macd_signal_9") is False
    assert research_freeze_text_has_trade_or_execution_language("we should buy now") is True
    assert research_freeze_text_has_trade_or_execution_language("kesin sat") is True
