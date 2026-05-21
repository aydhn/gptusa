def test_audit():
    from usa_signal_bot.paper_promotion_dossier.dossier_audit import create_promotion_dossier_audit_entry
    e = create_promotion_dossier_audit_entry("Type", "ID1", "ACTION", "Rationale")
    assert e.entity_id == "ID1"
