
from usa_signal_bot.cost_robustness.fee_stress import build_fee_stress_scenarios
def test_fee():
    assert len(build_fee_stress_scenarios()) > 0
