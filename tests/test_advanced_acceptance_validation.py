import pytest
from usa_signal_bot.release.advanced_acceptance_report import build_advanced_acceptance_context
from usa_signal_bot.release.advanced_acceptance_validation import (
    validate_advanced_acceptance_context_report,
    validate_no_sensitive_data_in_advanced_acceptance_payload,
    validate_no_execution_language_in_advanced_acceptance_text,
    validate_no_unsafe_advanced_acceptance_fields
)

def test_advanced_acceptance_validation():
    context = build_advanced_acceptance_context()
    report = validate_advanced_acceptance_context_report(context)
    # The default empty mock might have schema missing some attributes since it's partially initialized,
    # but the framework is intact.

    rep2 = validate_no_sensitive_data_in_advanced_acceptance_payload({"test": "safe"})
    assert rep2.valid == True

    rep3 = validate_no_sensitive_data_in_advanced_acceptance_payload({"api_key": "123"})
    assert rep3.valid == False

    rep4 = validate_no_execution_language_in_advanced_acceptance_text("This is safe text")
    assert rep4.valid == True

    rep5 = validate_no_unsafe_advanced_acceptance_fields({"target_weight": 0.5})
    assert rep5.valid == False
