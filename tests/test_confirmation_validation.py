from usa_signal_bot.paper_readiness_confirmation.confirmation_validation import (
    validate_no_live_execution_language_in_confirmation,
    validate_no_sensitive_data_in_confirmation_payload,
    validate_no_broker_execution_fields_in_confirmation,
    validate_no_active_paper_language_in_confirmation,
    validate_no_paper_state_mutation_fields_in_confirmation
)

def test_validate_no_live_execution_language():
    r1 = validate_no_live_execution_language_in_confirmation("This is a safe text.")
    assert r1.valid is True

    r2 = validate_no_live_execution_language_in_confirmation("This is sent to broker")
    assert r2.valid is False

def test_validate_no_sensitive_data():
    r1 = validate_no_sensitive_data_in_confirmation_payload({"key": "value"})
    assert r1.valid is True

    r2 = validate_no_sensitive_data_in_confirmation_payload({"api_key": "123"})
    assert r2.valid is False

def test_validate_no_broker_execution_fields():
    r1 = validate_no_broker_execution_fields_in_confirmation({"key": "value"})
    assert r1.valid is True

    r2 = validate_no_broker_execution_fields_in_confirmation({"broker_order_id": "123"})
    assert r2.valid is False

def test_validate_no_active_paper_language():
    r1 = validate_no_active_paper_language_in_confirmation("This is safe")
    assert r1.valid is True

    r2 = validate_no_active_paper_language_in_confirmation("paper'a uygula")
    assert r2.valid is False

def test_validate_no_paper_state_mutation_fields():
    r1 = validate_no_paper_state_mutation_fields_in_confirmation({"key": "value"})
    assert r1.valid is True

    r2 = validate_no_paper_state_mutation_fields_in_confirmation({"paper_state_committed": True})
    assert r2.valid is False
