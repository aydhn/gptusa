from usa_signal_bot.paper_observation.window_planner import default_observation_window
from usa_signal_bot.paper_observation.window_tracker import (
    update_observation_window_with_session, update_observation_window_with_checkpoint,
    observation_window_completed, observation_window_expired, observation_window_blocked,
    observation_window_tracker_summary, observation_window_tracker_to_text
)
import datetime

def test_window_tracker():
    window = default_observation_window("c1", "t1")
    window.required_session_count = 1

    assert observation_window_completed(window) is False

    window = update_observation_window_with_session(window, {"session_id": "s1"})
    assert "s1" in window.dry_run_session_ids
    assert observation_window_completed(window) is True

    window = update_observation_window_with_checkpoint(window, {"checkpoint_id": "cp1"})
    assert "cp1" in window.checkpoint_ids

    assert observation_window_blocked(window) is False

    now = datetime.datetime.now(datetime.timezone.utc)
    future = (now + datetime.timedelta(days=10)).isoformat()
    assert observation_window_expired(window, future) is True

    summary = observation_window_tracker_summary(window)
    assert summary["completed"] is True

    text = observation_window_tracker_to_text(window)
    assert "Yes" in text
