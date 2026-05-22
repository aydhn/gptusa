from usa_signal_bot.paper_dry_admission.dry_admission_audit import create_dry_admission_audit_entry

def test_dry_admission_audit():
    entry = create_dry_admission_audit_entry("Entity", "id1", "ACTION", "rationale")
    assert entry.entity_type == "Entity"
    assert entry.action == "ACTION"
