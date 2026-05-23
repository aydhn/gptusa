
from usa_signal_bot.paper_no_write_transition.sandbox_bridge_envelope import build_default_paper_sandbox_bridge_envelope
def test_bridge_envelope():
    assert build_default_paper_sandbox_bridge_envelope() is not None
