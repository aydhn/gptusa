import pytest
from usa_signal_bot.transaction_costs.paper_adapter import apply_transaction_costs_to_paper_order, apply_transaction_costs_to_paper_fill

def test_paper_order_adapter():
    order = {"symbol": "SPY", "action": "buy", "quantity": 10, "limit_price": 100.0}
    adj = apply_transaction_costs_to_paper_order(order, None, {"transaction_cost_model": {"enabled": True}})
    assert "estimated_cost_usd" in adj

def test_paper_fill_adapter():
    fill = {"symbol": "SPY", "action": "buy", "quantity": 10, "fill_price": 100.0}
    adj = apply_transaction_costs_to_paper_fill(fill, {"transaction_cost_model": {"enabled": True}})
    assert "cost_adjusted_fill_price" in adj
