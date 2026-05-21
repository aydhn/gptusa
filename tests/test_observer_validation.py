from usa_signal_bot.paper_observer.observer_validation import (
    validate_observer_enrollment_report,
    validate_no_live_execution_language_in_observer,
    validate_no_broker_execution_fields_in_observer
)
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment

def test_validate_observer_enrollment_report():
    enrollment = build_observer_enrollment("cand_1", "ticket_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    report = validate_observer_enrollment_report(enrollment)
    assert report.valid is True

    enrollment.allowed_for_active_paper = True
    report = validate_observer_enrollment_report(enrollment)
    assert report.valid is False
    assert report.blocked_count == 1

def test_validate_no_live_execution_language():
    report = validate_no_live_execution_language_in_observer("Bu kesin al garantidir")
    assert report.valid is False
    assert report.blocked_count > 0

def test_validate_no_broker_execution_fields():
    report = validate_no_broker_execution_fields_in_observer({"broker_order_id": "123"})
    assert report.valid is False
    assert report.blocked_count == 1
