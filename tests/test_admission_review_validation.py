from usa_signal_bot.paper_admission_review.admission_review_validation import (
    validate_no_live_execution_language_in_admission,
    validate_no_active_paper_language_in_admission,
    validate_no_broker_execution_fields_in_admission,
    validate_no_paper_state_mutation_fields_in_admission
)

def test_validate_no_live_execution_language():
    text = "Here we sent to broker and live approved"
    report = validate_no_live_execution_language_in_admission(text)
    assert not report.valid
    assert report.error_count > 0

    clean_text = "Just a review"
    report = validate_no_live_execution_language_in_admission(clean_text)
    assert report.valid

def test_validate_no_broker_execution_fields():
    payload = {"broker_order_id": "123"}
    report = validate_no_broker_execution_fields_in_admission(payload)
    assert not report.valid

    clean_payload = {"dry_run": True}
    report = validate_no_broker_execution_fields_in_admission(clean_payload)
    assert report.valid
