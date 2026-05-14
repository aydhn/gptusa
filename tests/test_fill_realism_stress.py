
from usa_signal_bot.cost_robustness.fill_realism_stress import build_fill_realism_stress_scenarios
def test_fill():
    assert len(build_fill_realism_stress_scenarios()) > 0
