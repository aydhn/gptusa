from usa_signal_bot.paper_observer.observer_reporting import observer_enrollment_to_text
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment

def test_observer_enrollment_to_text():
    enrollment = build_observer_enrollment("cand_1", "ticket_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    text = observer_enrollment_to_text(enrollment)
    assert enrollment.enrollment_id in text
    assert enrollment.status.value in text
