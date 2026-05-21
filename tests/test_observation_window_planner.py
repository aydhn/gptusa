from usa_signal_bot.paper_observation.window_planner import build_observation_window, default_observation_window, observation_window_end_at, validate_observation_window_plan, observation_window_plan_summary, observation_window_plan_to_text

def test_window_planner():
    window = build_observation_window({"candidate_id": "c1", "ticket_id": "t1"}, None, 3, 7)
    assert window.candidate_id == "c1"
    assert window.ticket_id == "t1"
    assert window.required_session_count == 3
    assert window.allows_active_paper is False

    def_win = default_observation_window("c2", "t2")
    assert def_win.candidate_id == "c2"

    end_dt = observation_window_end_at(7)
    assert end_dt is not None

    errors = validate_observation_window_plan(window)
    assert len(errors) == 0

    summary = observation_window_plan_summary(window)
    assert summary["candidate_id"] == "c1"

    text = observation_window_plan_to_text(window)
    assert "c1" in text
