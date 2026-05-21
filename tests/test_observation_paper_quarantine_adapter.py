from usa_signal_bot.paper_observation.paper_quarantine_adapter import (
    observation_window_from_quarantine_review, quarantine_exit_review_from_quarantine_payload,
    attach_observation_review_to_quarantine_payload, paper_quarantine_observation_summary,
    paper_quarantine_adapter_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_paper_quarantine_adapter():
    payload = {"candidate_id": "c1", "status": "ENROLLED"}
    win = observation_window_from_quarantine_review(payload)
    assert win.candidate_id == "c1"

    exit_rev = quarantine_exit_review_from_quarantine_payload(payload, {"telemetry_events": []})
    assert exit_rev.candidate_id == "c1"

    rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [], [], [], [], [], [], {})
    pl = attach_observation_review_to_quarantine_payload(payload.copy(), rev)
    assert pl["observation_review_id"] == "r1"

    summ = paper_quarantine_observation_summary(payload)
    assert summ["quarantine_status"] == "ENROLLED"

    text = paper_quarantine_adapter_to_text(payload)
    assert "Adapter Info" in text
