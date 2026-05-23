
from usa_signal_bot.paper_no_write_transition.transition_validation import validate_no_sensitive_data_in_transition_payload
def test_validation():
    assert validate_no_sensitive_data_in_transition_payload({}).valid
