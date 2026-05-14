
from usa_signal_bot.cost_robustness.participation_stress import build_participation_stress_scenarios
def test_participation():
    assert len(build_participation_stress_scenarios()) > 0
