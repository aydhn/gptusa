from usa_signal_bot.paper_no_write_admission.eligibility_checker import *
def test_eligibility_checker():
    assert evaluate_no_write_admission_eligibility({}) is not None
