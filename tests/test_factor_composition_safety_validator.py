import pytest
from usa_signal_bot.feature_engine.factor_composition.factor_composition_safety_validator import (
    factor_composition_text_has_trade_or_execution_language,
    validate_factor_feature_columns_safety
)

def test_factor_composition_text_has_trade_or_execution_language():
    assert factor_composition_text_has_trade_or_execution_language("this is a buy signal") is True
    assert factor_composition_text_has_trade_or_execution_language("this is a strong sell") is True
    assert factor_composition_text_has_trade_or_execution_language("research factor trend") is False

def test_validate_factor_feature_columns_safety():
    assert len(validate_factor_feature_columns_safety(["returns_1d", "macd_signal"])) == 0
    assert len(validate_factor_feature_columns_safety(["buy_flag"])) > 0
