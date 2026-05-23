
from usa_signal_bot.paper_no_order_dossier.admission_blocker_analyzer import analyze_admission_blocker_events
from usa_signal_bot.paper_no_order_dossier.admission_attempt_simulator import simulate_paper_admission_attempts

def test_analyze_admission_blocker_events_shows_all_blocked():
    events = simulate_paper_admission_attempts()
    res = analyze_admission_blocker_events(events)
    assert res["summary"]["all_blocked"] is True
