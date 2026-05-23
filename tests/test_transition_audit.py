
from usa_signal_bot.paper_no_write_transition.transition_audit import create_no_write_transition_audit_entry
def test_audit():
    assert create_no_write_transition_audit_entry("test", "id", "action", "rationale") is not None
