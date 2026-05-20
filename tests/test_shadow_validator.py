from usa_signal_bot.paper_shadow.shadow_validator import (
    validate_shadow_session_safety, validate_shadow_session_no_real_orders,
    validate_shadow_session_no_paper_mutation, validate_shadow_session_no_real_telegram,
    shadow_validator_summary
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def test_validate_shadow_session_safety():
    session = ShadowRehearsalSession(
        session_id="s1", created_at_utc="", status="COMPLETED",
        context=build_mock_shadow_simulation_context(), portfolio_state=None,
        signals=[], order_intents=[], fills=[], ledger_events=[], pnl_snapshots=[],
        safety_flags=[], started_at_utc=None, completed_at_utc=None,
        output_paths={}, warnings=[], errors=[]
    )
    errors = validate_shadow_session_safety(session)
    assert len(errors) == 0

    session.context.allow_real_orders = True
    errors = validate_shadow_session_safety(session)
    assert len(errors) == 1
