
from usa_signal_bot.cost_robustness.spread_stress import build_spread_stress_scenarios
def test_spread():
    assert len(build_spread_stress_scenarios()) > 0
