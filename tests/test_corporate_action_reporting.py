"""Test corporate action reporting."""
from usa_signal_bot.corporate_actions.corporate_action_reporting import corporate_action_limitations_text

def test_corporate_action_reporting():
    txt = corporate_action_limitations_text()
    assert "DO NOT constitute investment advice" in txt
