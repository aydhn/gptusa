
from usa_signal_bot.paper_no_write_transition.transition_store import no_write_transition_store_summary
from pathlib import Path
def test_store():
    assert isinstance(no_write_transition_store_summary(Path("/tmp")), dict)
