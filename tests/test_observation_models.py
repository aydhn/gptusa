import pytest
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationWindowStatus, ObservationWindowMode
from usa_signal_bot.paper_observation.observation_validation import assert_observation_valid

def test_observation_window_valid():
    w = ObservationWindow(
        window_id="w1", created_at_utc="2023", candidate_id="c1", ticket_id="t1",
        status=ObservationWindowStatus.DRAFT, mode=ObservationWindowMode.FULL_SUPERVISED_OBSERVATION,
        started_at_utc=None, ends_at_utc=None, required_session_count=3, observed_session_count=0,
        dry_run_session_ids=[], checkpoint_ids=[], telemetry_event_count=0, blocked_operation_count=0,
        manual_review_required=False
    )
    assert w.allows_active_paper is False
    assert_observation_valid(w)

def test_observation_window_invalid():
    w = ObservationWindow(
        window_id="w1", created_at_utc="2023", candidate_id="c1", ticket_id="t1",
        status=ObservationWindowStatus.DRAFT, mode=ObservationWindowMode.FULL_SUPERVISED_OBSERVATION,
        started_at_utc=None, ends_at_utc=None, required_session_count=3, observed_session_count=0,
        dry_run_session_ids=[], checkpoint_ids=[], telemetry_event_count=0, blocked_operation_count=0,
        manual_review_required=False, allows_active_paper=True
    )
    with pytest.raises(ValueError, match="allows_active_paper MUST be False"):
        assert_observation_valid(w)
