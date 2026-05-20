from usa_signal_bot.paper_shadow.shadow_fill_simulator import (
    simulate_shadow_fill, simulate_shadow_fills, reject_blocked_intent_fill,
    validate_shadow_fills_safe, shadow_fill_summary, shadow_fills_to_text
)
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intent_from_signal

def test_simulate_shadow_fill():
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    intent.status = "RISK_APPROVED"
    fill = simulate_shadow_fill(intent)
    assert fill.status == "SIMULATED_FILLED"
    assert not fill.is_real_fill

def test_reject_blocked_intent_fill():
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    intent.status = "BLOCKED"
    fill = simulate_shadow_fill(intent)
    assert fill.status == "BLOCKED"

def test_validate_shadow_fills_safe():
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    intent.status = "RISK_APPROVED"
    fill = simulate_shadow_fill(intent)
    assert len(validate_shadow_fills_safe([fill])) == 0
    fill.is_real_fill = True
    assert len(validate_shadow_fills_safe([fill])) == 1

def test_shadow_fill_summary():
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    intent.status = "RISK_APPROVED"
    fill = simulate_shadow_fill(intent)
    s = shadow_fill_summary([fill])
    assert s["filled"] == 1
