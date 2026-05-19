import pytest
from usa_signal_bot.paper_shadow.shadow_ledger import (
    create_shadow_ledger_event,
    build_ledger_from_shadow_session,
    append_shadow_ledger_event,
    shadow_ledger_to_text
)
from usa_signal_bot.core.enums import ShadowLedgerEventType
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from datetime import datetime, timezone

def test_shadow_ledger():
    ev = create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {"key": "val"})
    assert ev.event_type == ShadowLedgerEventType.SESSION_STARTED

    ev_secret = create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {"secret_key": "val"})
    assert "secret_key" not in ev_secret.payload

    from usa_signal_bot.core.enums import ShadowSessionStatus
    sess = ShadowRehearsalSession(
        session_id="test",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=ShadowSessionStatus.COMPLETED,
        signals=[],
        order_intents=[],
        fills=[],
        ledger_events=[],
        pnl_snapshots=[],
        safety_flags=[],
        output_paths={},
        warnings=[],
        errors=[]
    )
    ledger = build_ledger_from_shadow_session(sess)
    assert len(ledger) == 2 # start, complete

    ledger = append_shadow_ledger_event(ledger, ev)
    assert len(ledger) == 3

    text = shadow_ledger_to_text(ledger)
    assert "Shadow Ledger" in text
