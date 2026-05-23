
from usa_signal_bot.paper_no_write_transition.sandbox_bridge_safety_validator import validate_sandbox_bridge_safety
from usa_signal_bot.paper_no_write_transition.sandbox_bridge_envelope import build_default_paper_sandbox_bridge_envelope
def test_bridge_safety():
    env = build_default_paper_sandbox_bridge_envelope()
    assert isinstance(validate_sandbox_bridge_safety(envelope=env), list)
