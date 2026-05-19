import pytest
from usa_signal_bot.paper_shadow.result_analyzer import (
    analyze_shadow_rehearsal_session,
    shadow_result_analyzer_to_text
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.core.enums import ShadowSessionStatus
from datetime import datetime, timezone

def test_shadow_result_analyzer():
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

    res = analyze_shadow_rehearsal_session(sess)
    assert "metrics" in res
    assert "SESSION_COMPLETED" in res["success_flags"]

    text = shadow_result_analyzer_to_text(res)
    assert "Shadow Result Analysis" in text
