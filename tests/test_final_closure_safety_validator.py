import pytest
from usa_signal_bot.feature_engine.final_closure.final_closure_safety_validator import (
    validate_final_closure_columns_safety,
    final_closure_text_has_trade_or_execution_language
)

def test_validate_final_closure_columns_safety():
    assert len(validate_final_closure_columns_safety(["price", "macd_signal_9"])) == 0
    assert len(validate_final_closure_columns_safety(["buy_signal"])) > 0
    assert len(validate_final_closure_columns_safety(["portfolio_weight"])) > 0

def test_final_closure_text_has_trade_or_execution_language():
    assert final_closure_text_has_trade_or_execution_language("This is a safe report.") is False
    assert final_closure_text_has_trade_or_execution_language("kesin al") is True
    assert final_closure_text_has_trade_or_execution_language("buy signal tespit edildi") is True
