import pytest
from usa_signal_bot.paper_observer.controlled_planning_ingestion import (
    ingest_controlled_planning_review,
    extract_planning_ticket_payload,
    extract_final_approval_queue_item,
    extract_planning_candidate_id,
    extract_approval_status,
    controlled_planning_supports_observer
)
from usa_signal_bot.core.exceptions import ObserverControlledPlanningIngestionError

def test_ingest_controlled_planning_review_valid():
    payload = {
        "report_type": "FULL_CONTROLLED_PLANNING_REVIEW",
        "planning_ticket": {"candidate_id": "cand_123"},
        "final_approval": {"status": "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE"}
    }
    result = ingest_controlled_planning_review(payload)
    assert result == payload

    assert extract_planning_candidate_id(result) == "cand_123"
    assert extract_approval_status(result) == "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE"

    supports, warnings = controlled_planning_supports_observer(result)
    assert supports is True
    assert len(warnings) == 0

def test_ingest_controlled_planning_review_invalid():
    with pytest.raises(ObserverControlledPlanningIngestionError):
        ingest_controlled_planning_review({"missing": "report_type"})

def test_controlled_planning_supports_observer_rejected():
    payload = {"final_approval": {"status": "REJECTED"}}
    supports, warnings = controlled_planning_supports_observer(payload)
    assert supports is False
    assert len(warnings) == 1
    assert "REJECTED" in warnings[0]
