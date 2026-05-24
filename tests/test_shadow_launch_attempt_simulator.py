from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_attempt_simulator import simulate_shadow_launch_attempts

def test_simulate_shadow_launch_attempts():
    events = simulate_shadow_launch_attempts()
    assert len(events) == 11
    assert all(e.blocked for e in events)
