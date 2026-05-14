
from usa_signal_bot.cost_robustness.impact_stress import build_market_impact_stress_scenarios
def test_impact():
    assert len(build_market_impact_stress_scenarios()) > 0
