from usa_signal_bot.paper_observer.controlled_planning_adapter import (
    observer_enrollment_from_controlled_planning_review,
    observer_runtime_session_from_controlled_planning_review,
    observer_review_from_controlled_planning_review,
    attach_observer_metadata_to_controlled_planning_payload
)

def test_controlled_planning_adapter():
    payload = {
        "report_type": "FULL_CONTROLLED_PLANNING_REVIEW",
        "planning_ticket": {"ticket_id": "t1", "candidate_id": "cand_1"},
        "final_approval": {"item_id": "a1", "status": "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE"}
    }

    enrollment = observer_enrollment_from_controlled_planning_review(payload)
    assert enrollment.candidate_id == "cand_1"

    session = observer_runtime_session_from_controlled_planning_review(payload, {"signal_count": 0})
    assert len(session.outputs) > 0

    review = observer_review_from_controlled_planning_review(payload)
    assert len(review.enrollments) == 1

    new_payload = attach_observer_metadata_to_controlled_planning_payload(payload, review)
    assert "paper_observer_metadata" in new_payload
    assert new_payload["paper_observer_metadata"]["review_id"] == review.review_id
