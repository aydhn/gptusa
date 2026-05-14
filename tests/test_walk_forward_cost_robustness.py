
from usa_signal_bot.cost_robustness.walk_forward_cost_robustness import evaluate_walk_forward_cost_robustness
def test_wf():
    res = evaluate_walk_forward_cost_robustness({})
    assert res is not None
