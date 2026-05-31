from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_validation import validate_no_sensitive_data_in_research_freeze_payload

def test_validate_no_sensitive_data_in_research_freeze_payload():
    rep = validate_no_sensitive_data_in_research_freeze_payload({"a": 1})
    assert rep.valid is True
    rep = validate_no_sensitive_data_in_research_freeze_payload({"api_key": "123"})
    assert rep.valid is False
