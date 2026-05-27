import pytest
from usa_signal_bot.feature_engine.factor_composition.factor_composition_validation import (
    validate_no_sensitive_data_in_factor_composition_payload,
    validate_no_unsafe_factor_composition_fields,
    validate_no_execution_language_in_factor_composition_text
)

def test_validate_no_sensitive_data():
    rep = validate_no_sensitive_data_in_factor_composition_payload({"api_key": "123"})
    assert rep.valid is False
    assert any("api_key" in e for e in rep.errors)

def test_validate_no_unsafe_fields():
    rep = validate_no_unsafe_factor_composition_fields({"activation_allowed": True})
    assert rep.valid is False
    assert any("activation_allowed" in e for e in rep.errors)

def test_validate_no_execution_language():
    rep = validate_no_execution_language_in_factor_composition_text("We will send a buy signal.")
    assert rep.valid is False
