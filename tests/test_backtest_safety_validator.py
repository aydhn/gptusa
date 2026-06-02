import pytest
from usa_signal_bot.backtesting.backtest_safety_validator import backtest_text_has_trade_or_execution_language

def test_language_validator():
    assert backtest_text_has_trade_or_execution_language("send_to_telegram now") is True
    assert backtest_text_has_trade_or_execution_language("this is a research test") is False
