
from usa_signal_bot.paper_no_write_transition.dry_admission_adapter import dry_admission_transition_summary
def test_dry_adapter():
    assert "status" in dry_admission_transition_summary({})
