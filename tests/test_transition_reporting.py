
from usa_signal_bot.paper_no_write_transition.transition_reporting import no_write_transition_limitations_text
def test_reporting():
    assert len(no_write_transition_limitations_text()) > 0
