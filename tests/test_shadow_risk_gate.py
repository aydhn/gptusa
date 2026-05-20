from usa_signal_bot.paper_shadow.shadow_risk_gate import (
    evaluate_shadow_order_risk, apply_shadow_risk_gates,
    shadow_risk_gate_warnings, shadow_risk_gate_summary, shadow_risk_gate_to_text
)
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intent_from_signal
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio

def test_evaluate_shadow_order_risk():
    ctx = build_mock_shadow_simulation_context(100000.0)
    port = initialize_shadow_portfolio(ctx)
    signals = generate_mock_shadow_signals(["AAPL"])

    # Normal
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    assert evaluate_shadow_order_risk(intent, port, ctx) == "PASS"

    # Oversize
    intent = build_shadow_order_intent_from_signal(signals[0], 10000.0, 100.0)
    assert evaluate_shadow_order_risk(intent, port, ctx) == "WARNING"

def test_apply_shadow_risk_gates():
    ctx = build_mock_shadow_simulation_context(100000.0)
    port = initialize_shadow_portfolio(ctx)
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)

    gated = apply_shadow_risk_gates([intent], port, ctx)
    assert gated[0].status == "RISK_APPROVED"

def test_shadow_risk_gate_summary():
    ctx = build_mock_shadow_simulation_context(100000.0)
    port = initialize_shadow_portfolio(ctx)
    signals = generate_mock_shadow_signals(["AAPL"])
    intent = build_shadow_order_intent_from_signal(signals[0], 1000.0, 100.0)
    gated = apply_shadow_risk_gates([intent], port, ctx)
    s = shadow_risk_gate_summary(gated)
    assert s["approved"] == 1
