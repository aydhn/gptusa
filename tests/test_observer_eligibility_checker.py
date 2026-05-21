from usa_signal_bot.paper_observer.eligibility_checker import (
    evaluate_observer_enrollment_eligibility,
    observer_safety_flags_from_controlled_planning
)
from usa_signal_bot.core.enums import PaperObserverEnrollmentStatus, ObserverSafetyFlag

def test_evaluate_eligibility_approved():
    payload = {
        "planning_ticket": {"ticket_id": "1"},
        "final_approval": {"status": "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE"}
    }
    status = evaluate_observer_enrollment_eligibility(payload)
    assert status == PaperObserverEnrollmentStatus.ELIGIBLE

def test_evaluate_eligibility_waiting():
    payload = {
        "final_approval": {"status": "WAITING_REVIEW"}
    }
    status = evaluate_observer_enrollment_eligibility(payload)
    assert status == PaperObserverEnrollmentStatus.DRAFT

def test_evaluate_eligibility_rejected():
    payload = {
        "final_approval": {"status": "REJECTED"}
    }
    status = evaluate_observer_enrollment_eligibility(payload)
    assert status == PaperObserverEnrollmentStatus.REJECTED

def test_safety_flags():
    payload = {"final_approval": {"status": "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE"}}
    flags = observer_safety_flags_from_controlled_planning(payload)
    assert ObserverSafetyFlag.MISSING_PLANNING_TICKET in flags
