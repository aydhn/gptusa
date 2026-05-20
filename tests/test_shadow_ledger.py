from usa_signal_bot.paper_shadow.shadow_ledger import (
    create_shadow_ledger_event, build_ledger_from_shadow_session,
    append_shadow_ledger_event, shadow_ledger_summary, shadow_ledger_to_text
)
from usa_signal_bot.core.enums import ShadowLedgerEventType

def test_create_shadow_ledger_event():
    event = create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {"key": "val", "secret_token": "123"})
    assert event.event_type == "SESSION_STARTED"
    # Secret should be stripped
    assert "secret_token" not in event.payload

def test_append_shadow_ledger_event():
    event = create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {})
    events = append_shadow_ledger_event([], event)
    assert len(events) == 1

def test_shadow_ledger_summary():
    event1 = create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {})
    event2 = create_shadow_ledger_event(ShadowLedgerEventType.SESSION_COMPLETED, {})
    s = shadow_ledger_summary([event1, event2])
    assert s["started"]
    assert s["completed"]
