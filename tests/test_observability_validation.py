from usa_signal_bot.observability.observability_validation import validate_no_live_execution_language_in_observability

def test_validation():
    r = validate_no_live_execution_language_in_observability("Live approved!")
    assert not r.valid
    assert r.blocked_count == 1
