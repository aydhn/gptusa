from usa_signal_bot.paper_shadow.session_registry import (
    register_shadow_session, find_shadow_session_by_id, find_shadow_sessions_by_bundle_id,
    latest_shadow_session_for_bundle, shadow_session_registry_summary
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def test_session_registry():
    ctx = build_mock_shadow_simulation_context()
    ctx.source_bundle_id = "b1"
    session = ShadowRehearsalSession(
        session_id="s1", created_at_utc="2023-01-01T00:00:00Z", status="COMPLETED",
        context=ctx, portfolio_state=None, signals=[], order_intents=[], fills=[],
        ledger_events=[], pnl_snapshots=[], safety_flags=[], started_at_utc=None,
        completed_at_utc=None, output_paths={}, warnings=[], errors=[]
    )
    registry = register_shadow_session(session)
    assert len(registry) == 1
    assert find_shadow_session_by_id(registry, "s1") is not None
    assert len(find_shadow_sessions_by_bundle_id(registry, "b1")) == 1
    latest = latest_shadow_session_for_bundle(registry, "b1")
    assert latest.session_id == "s1"
