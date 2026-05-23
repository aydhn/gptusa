
from usa_signal_bot.paper_no_write_transition.admission_adapter import admission_transition_summary
def test_admission_adapter():
    assert "status" in admission_transition_summary({})
