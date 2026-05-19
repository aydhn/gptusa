import pytest
from usa_signal_bot.paper_shadow.session_registry import (
    register_shadow_session,
    find_shadow_session_by_id,
    shadow_session_registry_to_text
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.core.enums import ShadowSessionStatus
from datetime import datetime, timezone

def test_shadow_session_registry():
    sess = ShadowRehearsalSession(
        session_id="test_id",
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

    reg = register_shadow_session(sess)
    assert len(reg) == 1

    found = find_shadow_session_by_id(reg, "test_id")
    assert found is not None
    assert found.session_id == "test_id"

    text = shadow_session_registry_to_text(reg)
    assert "Shadow Session Registry" in text
