from usa_signal_bot.paper_controlled_planning.observation_ingestion import (
    ingest_observation_review, extract_quarantine_exit_review, extract_exit_decision,
    extract_observation_score, observation_supports_controlled_planning
)
from usa_signal_bot.core.exceptions import ControlledPlanningObservationIngestionError
import pytest

def test_ingestion():
    with pytest.raises(ControlledPlanningObservationIngestionError):
        ingest_observation_review({})

    p = {"candidate_id": "123", "quarantine_exit_review": {"decision": "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING"}}
    assert ingest_observation_review(p) == p
    assert extract_quarantine_exit_review(p) == {"decision": "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING"}
    assert extract_exit_decision(p) == "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING"
    supports, _ = observation_supports_controlled_planning(p)
    assert supports is True

    p_rej = {"exit_decision": "REJECT"}
    supports, _ = observation_supports_controlled_planning(p_rej)
    assert supports is False
