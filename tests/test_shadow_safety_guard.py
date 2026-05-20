import pytest
from usa_signal_bot.paper_shadow.shadow_safety_guard import (
    collect_shadow_safety_flags_from_context, collect_shadow_safety_flags_from_intents,
    collect_shadow_safety_flags_from_fills, shadow_session_has_blocking_flags,
    assert_shadow_session_safe, shadow_safety_summary
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intent_from_signal
from usa_signal_bot.core.exceptions import ShadowSafetyError

def test_collect_shadow_safety_flags_from_context():
    ctx = build_mock_shadow_simulation_context()
    assert len(collect_shadow_safety_flags_from_context(ctx)) == 0
    ctx.allow_real_orders = True
    flags = collect_shadow_safety_flags_from_context(ctx)
    assert "REAL_ORDER_RISK" in flags

def test_collect_shadow_safety_flags_from_intents():
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    assert len(collect_shadow_safety_flags_from_intents([intent])) == 0
    intent.is_real_order = True
    flags = collect_shadow_safety_flags_from_intents([intent])
    assert "REAL_ORDER_RISK" in flags

def test_assert_shadow_session_safe():
    ctx = build_mock_shadow_simulation_context()
    assert_shadow_session_safe(ctx) # should pass

    ctx.allow_real_orders = True
    with pytest.raises(ShadowSafetyError):
        assert_shadow_session_safe(ctx)
