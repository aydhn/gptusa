from usa_signal_bot.paper_readiness_confirmation.confirmation_audit import (
    create_readiness_confirmation_audit_entry,
    audit_entry_from_confirmation_queue_item
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item

def test_create_readiness_confirmation_audit_entry():
    entry = create_readiness_confirmation_audit_entry("TEST", "123", "ACTION", "Test rationale")
    assert entry.entity_type == "TEST"
    assert entry.entity_id == "123"
    assert entry.action == "ACTION"
    assert entry.rationale == "Test rationale"

def test_audit_entry_from_confirmation_queue_item():
    q = build_default_confirmation_queue_item("CAND1")
    entry = audit_entry_from_confirmation_queue_item(q)
    assert entry.entity_type == "QUEUE_ITEM"
    assert entry.entity_id == q.queue_item_id
    assert "CAND1" in entry.rationale
