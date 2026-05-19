import pytest
from usa_signal_bot.paper_shadow.shadow_order_intent import (
    build_shadow_order_intent_from_signal,
    build_shadow_order_intents,
    validate_shadow_order_intents_safe,
    block_real_order_like_intents,
    shadow_order_intents_to_text
)
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals

def test_shadow_order_intent():
    signal = generate_mock_shadow_signals(["AAPL"])[0]
    intent = build_shadow_order_intent_from_signal(signal, notional_usd=1000.0, price=100.0)

    assert intent.quantity == 10.0
    assert not intent.is_real_order
    assert intent.broker_destination is None

    errors = validate_shadow_order_intents_safe([intent])
    assert not errors

    intent.is_real_order = True
    errors = validate_shadow_order_intents_safe([intent])
    assert len(errors) == 1

    blocked = block_real_order_like_intents([intent])
    assert blocked[0].status.name == "BLOCKED"

    text = shadow_order_intents_to_text([intent])
    assert "Shadow Order Intents" in text
