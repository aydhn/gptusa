import pytest
from usa_signal_bot.regime_classification.validation.compatibility_validation_schema_validator import validate_no_forbidden_context_validation_columns

def test_validate_no_forbidden_columns():
    cols = ["symbol", "score", "buy_signal"]
    errs = validate_no_forbidden_context_validation_columns(cols)
    assert len(errs) > 0
    assert any("buy" in str(e) for e in errs)

def test_validate_no_forbidden_columns_safe():
    cols = ["symbol", "score", "macd_signal_9"]
    errs = validate_no_forbidden_context_validation_columns(cols)
    assert len(errs) == 0
