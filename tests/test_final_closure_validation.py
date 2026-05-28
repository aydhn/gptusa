import pytest
from usa_signal_bot.feature_engine.final_closure.final_closure_validation import (
    validate_no_sensitive_data_in_final_closure_payload,
    validate_no_execution_language_in_final_closure_text,
    validate_no_unsafe_final_closure_fields,
    assert_final_closure_validation_valid
)
from usa_signal_bot.core.exceptions import FinalClosureValidationError

def test_validate_no_sensitive_data_in_final_closure_payload():
    valid = validate_no_sensitive_data_in_final_closure_payload({"data": "normal"})
    assert valid.valid is True

    invalid = validate_no_sensitive_data_in_final_closure_payload({"api_key": "123"})
    assert invalid.valid is False

def test_validate_no_execution_language_in_final_closure_text():
    assert validate_no_execution_language_in_final_closure_text("hello").valid is True
    assert validate_no_execution_language_in_final_closure_text("strong buy").valid is False

def test_validate_no_unsafe_final_closure_fields():
    assert validate_no_unsafe_final_closure_fields({"activation_allowed": False}).valid is True
    assert validate_no_unsafe_final_closure_fields({"activation_allowed": True}).valid is False

def test_assert_final_closure_validation_valid():
    valid_report = validate_no_execution_language_in_final_closure_text("hello")
    assert_final_closure_validation_valid(valid_report)

    invalid_report = validate_no_execution_language_in_final_closure_text("strong buy")
    with pytest.raises(FinalClosureValidationError):
        assert_final_closure_validation_valid(invalid_report)
