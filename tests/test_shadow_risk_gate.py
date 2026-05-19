import pytest
from usa_signal_bot.paper_shadow.shadow_risk_gate import (
    evaluate_shadow_order_risk,
    apply_shadow_risk_gates,
    shadow_risk_gate_to_text
)
from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intent_from_signal
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio
from usa_signal_bot.core.enums import ShadowRiskGateStatus

def test_shadow_risk_gate():
    ctx = build_mock_shadow_simulation_context()
    port = initialize_shadow_portfolio(ctx)
    sig = generate_mock_shadow_signals(["AAPL"])[0]

    # Normal intent
    intent = build_shadow_order_intent_from_signal(sig, notional_usd=1000.0, price=100.0)
    status = evaluate_shadow_order_risk(intent, port, ctx)
    assert status == ShadowRiskGateStatus.PASS

    # Oversize intent (> 5% of 100k = 5k)
    intent2 = build_shadow_order_intent_from_signal(sig, notional_usd=6000.0, price=100.0)
    status2 = evaluate_shadow_order_risk(intent2, port, ctx)
    assert status2 == ShadowRiskGateStatus.WARNING

    applied = apply_shadow_risk_gates([intent, intent2], port, ctx)
    assert applied[0].status.name == "RISK_APPROVED"
    assert applied[1].status.name == "RISK_APPROVED"
    assert len(applied[1].warnings) == 1

    text = shadow_risk_gate_to_text({"total": 2})
    assert "Shadow Risk Gate Summary" in text
