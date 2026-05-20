from usa_signal_bot.paper_shadow.result_analyzer import (
    analyze_shadow_rehearsal_session, shadow_rehearsal_success_flags,
    shadow_rehearsal_warning_flags, shadow_rehearsal_block_flags, shadow_rehearsal_metrics
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def test_shadow_result_analyzer():
    session = ShadowRehearsalSession(
        session_id="s1", created_at_utc="2023-01-01T00:00:00Z", status="COMPLETED",
        context=None, portfolio_state=None, signals=[], order_intents=[], fills=[],
        ledger_events=[], pnl_snapshots=[], safety_flags=[], started_at_utc=None,
        completed_at_utc=None, output_paths={}, warnings=[], errors=[]
    )
    analysis = analyze_shadow_rehearsal_session(session)
    assert "SESSION_COMPLETED" in analysis["success_flags"]
    assert analysis["metrics"]["simulated_fill_count"] == 0
