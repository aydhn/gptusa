
from usa_signal_bot.cost_robustness.robustness_validation import validate_no_live_execution_language_in_cost_robustness
def test_validation():
    rep = validate_no_live_execution_language_in_cost_robustness("live approved")
    assert not rep.valid
