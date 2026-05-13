"""Test corporate action validation."""
from usa_signal_bot.corporate_actions.corporate_action_validation import validate_no_sensitive_data_in_corporate_action_payload

def test_corporate_action_validation():
    rep = validate_no_sensitive_data_in_corporate_action_payload({"data": "my_secret_token"})
    assert rep.valid is False
