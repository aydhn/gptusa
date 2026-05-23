
from usa_signal_bot.paper_no_write_transition.no_write_adapter import no_write_transition_summary
def test_no_write_adapter():
    assert "status" in no_write_transition_summary({})
