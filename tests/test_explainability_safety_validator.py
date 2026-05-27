import pytest
from usa_signal_bot.feature_engine.factor_explainability.explainability_safety_validator import explainability_text_has_trade_or_execution_language, validate_explainability_columns_safety

def test_explainability_text_has_trade_or_execution_language():
    assert explainability_text_has_trade_or_execution_language("buy") is True
    assert explainability_text_has_trade_or_execution_language("research observation") is False

def test_validate_explainability_columns_safety():
    assert len(validate_explainability_columns_safety(["order", "target_weight"])) == 2
    assert len(validate_explainability_columns_safety(["mom_10", "date"])) == 0
