import pytest
from usa_signal_bot.transaction_costs.basket_adapter import apply_transaction_costs_to_basket_result

def test_basket_adapter_enabled():
    res = {
        "trades": [{"symbol": "SPY", "quantity": 10, "entry_price": 100.0, "pnl_usd": 100.0}],
        "metrics": {"total_pnl": 100.0}
    }
    adjusted = apply_transaction_costs_to_basket_result(res, {"transaction_cost_model": {"enabled": True}})
    assert "net_pnl_usd" in adjusted["metrics"]
    assert adjusted["metrics"]["cost_adjusted"] is True
