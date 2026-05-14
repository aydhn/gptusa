
from usa_signal_bot.cost_robustness.fragility_detector import detect_cost_fragility
def test_fragility():
    res = detect_cost_fragility([])
    assert res is not None
