
from usa_signal_bot.cost_robustness.robustness_reporting import cost_robustness_limitations_text
def test_reporting():
    assert "LIMITATIONS" in cost_robustness_limitations_text()
