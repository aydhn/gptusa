from usa_signal_bot.paper_observer.observer_enrollment import (
    build_observer_enrollment_from_controlled_planning,
    validate_observer_enrollment_safety
)
from usa_signal_bot.core.enums import PaperObserverEnrollmentStatus, ObserverSafetyFlag

def test_build_enrollment_from_payload():
    payload = {
        "report_type": "FULL_CONTROLLED_PLANNING_REVIEW",
        "planning_ticket": {"ticket_id": "t1", "candidate_id": "cand_1"},
        "final_approval": {"item_id": "a1", "status": "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE"}
    }
    enrollment = build_observer_enrollment_from_controlled_planning(payload)

    assert enrollment.status == PaperObserverEnrollmentStatus.ELIGIBLE
    assert enrollment.candidate_id == "cand_1"
    assert enrollment.planning_ticket_id == "t1"
    assert enrollment.approval_queue_item_id == "a1"
    assert enrollment.allowed_for_active_paper is False
    assert enrollment.allowed_for_broker_execution is False

    errors = validate_observer_enrollment_safety(enrollment)
    assert len(errors) == 0

def test_validate_enrollment_safety_errors():
    enrollment = build_observer_enrollment_from_controlled_planning({})
    enrollment.allowed_for_active_paper = True

    errors = validate_observer_enrollment_safety(enrollment)
    assert len(errors) == 1
    assert "Enrollment cannot be allowed for active paper" in errors[0]
