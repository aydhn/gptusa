import pytest
from usa_signal_bot.core.enums import TransactionSide
from usa_signal_bot.transaction_costs.spread_cost import estimate_spread_cost_bps, estimate_spread_cost_usd, spread_cost_component

def test_half_spread_cost():
    bps = estimate_spread_cost_bps(10.0, TransactionSide.BUY)
    assert bps == 5.0

def test_spread_cost_usd():
    usd = estimate_spread_cost_usd(5.0, 1000)
    assert usd == 0.5

def test_spread_cost_component():
    comp = spread_cost_component("SPY", 20.0, TransactionSide.BUY, 1000)
    assert comp["spread_cost_bps"] == 10.0
    assert comp["spread_cost_usd"] == 1.0
