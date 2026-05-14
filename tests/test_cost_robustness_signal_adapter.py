
from usa_signal_bot.cost_robustness.signal_adapter import attach_cost_robustness_to_signal
def test_signal():
    assert attach_cost_robustness_to_signal({}) is not None
