
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_audit import create_no_order_dossier_audit_entry

def test_create_no_order_dossier_audit_entry():
    entry = create_no_order_dossier_audit_entry("Test", "t1", "TEST_ACTION", "Testing")
    assert entry.action == "TEST_ACTION"
