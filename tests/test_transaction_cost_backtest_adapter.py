import pytest
from usa_signal_bot.transaction_costs.backtest_adapter import apply_transaction_costs_to_backtest_trades

def test_backtest_adapter_disabled():
    trades = [{"symbol": "SPY", "pnl_usd": 100.0}]
    res = apply_transaction_costs_to_backtest_trades(trades, None, {"transaction_cost_model": {"enabled": False}})
    assert "net_pnl_usd" not in res[0]

def test_backtest_adapter_enabled():
    trades = [{"symbol": "SPY", "quantity": 10, "entry_price": 100.0, "pnl_usd": 100.0, "direction": "long"}]
    res = apply_transaction_costs_to_backtest_trades(trades, None, {"transaction_cost_model": {"enabled": True}})
    assert "net_pnl_usd" in res[0]
    assert res[0]["net_pnl_usd"] < res[0]["gross_pnl_usd"]
