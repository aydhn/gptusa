
from usa_signal_bot.cost_robustness.breakeven_costs import calculate_breakeven_total_cost_bps
def test_breakeven():
    res = calculate_breakeven_total_cost_bps([{"gross_pnl_usd": 100.0, "notional_value_usd": 10000.0}])
    assert res is not None
