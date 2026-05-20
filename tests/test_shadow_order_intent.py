from usa_signal_bot.paper_shadow.shadow_order_intent import (
    build_shadow_order_intent_from_signal, build_shadow_order_intents,
    validate_shadow_order_intents_safe, block_real_order_like_intents,
    shadow_order_intent_summary, shadow_order_intents_to_text
)
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals

def test_build_shadow_order_intent_from_signal():
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    assert intent.quantity == 10.0
    assert not intent.is_real_order

def test_build_shadow_order_intents():
    signals = generate_mock_shadow_signals()
    intents = build_shadow_order_intents(signals)
    assert len(intents) == 3

def test_validate_shadow_order_intents_safe():
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    assert len(validate_shadow_order_intents_safe([intent])) == 0
    intent.is_real_order = True
    assert len(validate_shadow_order_intents_safe([intent])) == 1

def test_block_real_order_like_intents():
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    intent.is_real_order = True
    blocked = block_real_order_like_intents([intent])
    assert blocked[0].status == "BLOCKED"

def test_shadow_order_intent_summary():
    signals = generate_mock_shadow_signals()
    intents = build_shadow_order_intents(signals, 1000.0)
    s = shadow_order_intent_summary(intents)
    assert s["total_notional_usd"] == 3000.0

def test_shadow_order_intents_to_text():
    signals = generate_mock_shadow_signals()
    intents = build_shadow_order_intents(signals, 1000.0)
    assert "count=3" in shadow_order_intents_to_text(intents)
