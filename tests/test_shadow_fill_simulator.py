import pytest
from usa_signal_bot.paper_shadow.shadow_fill_simulator import (
    simulate_shadow_fill,
    reject_blocked_intent_fill,
    validate_shadow_fills_safe,
    shadow_fills_to_text
)
from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intent_from_signal
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals

def test_shadow_fill_simulator():
    sig = generate_mock_shadow_signals(["AAPL"])[0]
    intent = build_shadow_order_intent_from_signal(sig, notional_usd=1000.0, price=100.0)

    fill = simulate_shadow_fill(intent)
    assert fill.status.name == "SIMULATED_FILLED"
    assert not fill.is_real_fill

    from usa_signal_bot.core.enums import ShadowOrderIntentStatus
    intent.status = ShadowOrderIntentStatus.BLOCKED
    fill2 = simulate_shadow_fill(intent)
    assert fill2.status.name == "BLOCKED"

    errors = validate_shadow_fills_safe([fill])
    assert not errors

    fill.is_real_fill = True
    errors = validate_shadow_fills_safe([fill])
    assert len(errors) == 1

    text = shadow_fills_to_text([fill])
    assert "Shadow Fills" in text
