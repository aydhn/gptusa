import pytest
from usa_signal_bot.release.advanced_acceptance_safety_validator import (
    advanced_acceptance_text_has_trade_or_execution_language,
    advanced_acceptance_payload_has_forbidden_fields
)

def test_safety_validator():
    assert advanced_acceptance_text_has_trade_or_execution_language("this is a live_order") == True
    assert advanced_acceptance_text_has_trade_or_execution_language("this is safe") == False

    assert advanced_acceptance_payload_has_forbidden_fields({"target_weight": 0.5}) == True
    assert advanced_acceptance_payload_has_forbidden_fields({"safe": 0.5}) == False
