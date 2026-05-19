import pytest
from usa_signal_bot.core.exceptions import ReleaseSandboxValidationError
from usa_signal_bot.release_sandbox.sandbox_validation import (
    validate_no_sensitive_data_in_sandbox_payload,
    validate_no_live_execution_language_in_sandbox,
    validate_no_auto_apply_or_production_language,
    validate_no_broker_execution_fields_in_sandbox,
    validate_no_paper_state_mutation_fields_in_sandbox,
    assert_release_sandbox_valid
)

def test_sandbox_validation_rules():
    res = validate_no_sensitive_data_in_sandbox_payload({"some_api_key": "123"})
    assert not res.valid

    res = validate_no_live_execution_language_in_sandbox("This is live approved")
    assert not res.valid

    res = validate_no_auto_apply_or_production_language("production'a geçir")
    assert not res.valid

    res = validate_no_broker_execution_fields_in_sandbox({"broker_order_id": "b1"})
    assert not res.valid

    res = validate_no_paper_state_mutation_fields_in_sandbox({"paper_state_committed": True})
    assert not res.valid

    with pytest.raises(ReleaseSandboxValidationError):
        assert_release_sandbox_valid(res)
