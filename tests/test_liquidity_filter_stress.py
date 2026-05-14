
from usa_signal_bot.cost_robustness.liquidity_filter_stress import build_liquidity_filter_stress_scenarios
def test_liquidity():
    assert len(build_liquidity_filter_stress_scenarios()) > 0
