
from usa_signal_bot.cost_robustness.basket_adapter import attach_cost_robustness_to_basket_result
def test_basket():
    assert attach_cost_robustness_to_basket_result({}) is not None
