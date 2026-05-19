import pytest
from usa_signal_bot.paper_shadow.shadow_validator import (
    validate_shadow_session_safety,
    shadow_validator_to_text
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.core.enums import ShadowSessionStatus
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from datetime import datetime, timezone

def test_shadow_validator():
    ctx = build_mock_shadow_simulation_context()
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
        errors=[],
        context=ctx
    )

    errors = validate_shadow_session_safety(sess)
    assert not errors

    ctx.allow_real_orders = True
    errors = validate_shadow_session_safety(sess)
    assert len(errors) == 1

    text = shadow_validator_to_text({"safety_errors": 1})
    assert "Shadow Validator Summary" in text
