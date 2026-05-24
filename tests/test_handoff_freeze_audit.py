import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_audit import create_handoff_freeze_audit_entry

def test_create_handoff_freeze_audit_entry():
    entry = create_handoff_freeze_audit_entry("Entity", "123", "EVALUATE", "Reason")
    assert entry.entity_type == "Entity"
    assert entry.action == "EVALUATE"
