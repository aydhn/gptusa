
from usa_signal_bot.paper_no_order_dossier.admission_attempt_simulator import simulate_paper_admission_attempts

def test_simulate_paper_admission_attempts_blocks_all():
    events = simulate_paper_admission_attempts()
    assert len(events) > 0
    for e in events:
        assert e.blocked is True
