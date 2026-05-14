
from usa_signal_bot.cost_robustness.slippage_stress import build_slippage_stress_scenarios
def test_slip():
    assert len(build_slippage_stress_scenarios()) > 0
