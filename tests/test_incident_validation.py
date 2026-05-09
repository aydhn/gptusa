from usa_signal_bot.incident.incident_validation import validate_no_live_execution_language_in_incident

def test_validation_live():
    rep = validate_no_live_execution_language_in_incident("This is live approved")
    assert not rep.valid
    rep2 = validate_no_live_execution_language_in_incident("This is just a local test")
    assert rep2.valid
