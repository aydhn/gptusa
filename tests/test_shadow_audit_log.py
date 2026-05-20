def test_audit():
    from usa_signal_bot.paper_shadow_governance.audit_log import create_shadow_governance_audit_entry
    e = create_shadow_governance_audit_entry("T", "I", "A", "R")
    assert e.entity_id == "I"
