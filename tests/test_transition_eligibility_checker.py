
from usa_signal_bot.paper_no_write_transition.eligibility_checker import evaluate_no_write_transition_eligibility
def test_eligibility():
    assert evaluate_no_write_transition_eligibility({}) is not None
