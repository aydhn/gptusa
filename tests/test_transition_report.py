
from usa_signal_bot.paper_no_write_transition.transition_report import build_no_write_transition_full_review
def test_report():
    assert build_no_write_transition_full_review({"candidate_id": "test"}) is not None
