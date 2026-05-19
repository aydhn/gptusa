import pytest
from usa_signal_bot.paper_shadow.shadow_notifications import (
    build_shadow_notification_preview,
    shadow_notification_to_text
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.core.enums import ShadowSessionStatus
from datetime import datetime, timezone

def test_shadow_notifications():
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

    prev = build_shadow_notification_preview(sess)
    assert "completed" in prev["message"]
    assert prev["is_safe"]

    text = shadow_notification_to_text(prev)
    assert "Shadow Notification Preview" in text
