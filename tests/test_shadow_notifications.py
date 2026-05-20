from usa_signal_bot.paper_shadow.shadow_notifications import (
    build_shadow_notification_preview, format_shadow_rehearsal_message,
    validate_shadow_notification_safe, shadow_notification_summary
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def test_build_shadow_notification_preview():
    session = ShadowRehearsalSession(
        session_id="s1", created_at_utc="", status="COMPLETED",
        context=None, portfolio_state=None, signals=[], order_intents=[],
        fills=[], ledger_events=[], pnl_snapshots=[], safety_flags=[],
        started_at_utc=None, completed_at_utc=None, output_paths={}, warnings=[], errors=[]
    )
    prev = build_shadow_notification_preview(session)
    assert not prev["is_real_send"]

def test_validate_shadow_notification_safe():
    assert len(validate_shadow_notification_safe({"is_real_send": False})) == 0
    assert len(validate_shadow_notification_safe({"is_real_send": True})) == 1
