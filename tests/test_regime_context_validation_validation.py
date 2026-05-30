import pytest
from usa_signal_bot.regime_classification.validation.regime_context_validation_validation import validate_no_unsafe_context_validation_fields

def test_validate_no_unsafe_context_validation_fields():
    rep = validate_no_unsafe_context_validation_fields({"buy_signal": True})
    assert rep.valid is False
