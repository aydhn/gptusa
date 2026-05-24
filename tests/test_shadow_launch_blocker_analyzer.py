from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_attempt_simulator import simulate_shadow_launch_attempts
from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_blocker_analyzer import analyze_shadow_launch_blocker_events

def test_analyze_shadow_launch_blocker_events():
    events = simulate_shadow_launch_attempts()
    res = analyze_shadow_launch_blocker_events(events)
    assert res["all_blocked"] is True
