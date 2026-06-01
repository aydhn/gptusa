import pytest
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_scaffolding_schema_validator import validate_baseline_scaffolding_column_names, validate_no_forbidden_baseline_scaffolding_columns
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_scaffolding_safety_validator import baseline_scaffolding_text_has_trade_or_execution_language

def test_baseline_scaffolding_schema_validator():
    errors = validate_baseline_scaffolding_column_names(["feature_1", "feature_2", "macd_signal_9", "buy"])
    assert len(errors) == 1
    assert "buy" in errors[0]

def test_baseline_scaffolding_safety_validator():
    is_unsafe = baseline_scaffolding_text_has_trade_or_execution_language("This is a guaranteed profit strategy.")
    assert is_unsafe is True

    is_unsafe2 = baseline_scaffolding_text_has_trade_or_execution_language("This model predicts the probability of positive returns.")
    assert is_unsafe2 is False
