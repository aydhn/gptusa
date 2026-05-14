
from usa_signal_bot.cost_robustness.robustness_score import calculate_cost_robustness_score
def test_score():
    assert calculate_cost_robustness_score([]) is None
