from usa_signal_bot.paper_no_write_admission.preflight_audit import *
def test_preflight_audit():
    res = create_no_write_admission_audit_entry("x", "y", "z", "w")
    assert res is not None
