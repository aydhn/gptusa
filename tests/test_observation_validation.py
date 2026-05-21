from usa_signal_bot.paper_observation.observation_validation import validate_no_live_execution_language_in_observation

def test_no_live_execution_language():
    res = validate_no_live_execution_language_in_observation("this is a test")
    assert res.valid is True

    res = validate_no_live_execution_language_in_observation("candidate kesin iyi alınmalı")
    assert res.valid is False
    assert "candidate kesin iyi" in res.errors[0]
