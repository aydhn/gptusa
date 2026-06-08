from usa_signal_bot.portfolio.foundation.portfolio_foundation_safety_validator import (
    portfolio_foundation_text_has_trade_or_execution_language, portfolio_payload_has_forbidden_fields
)

def test_text_safety():
    assert not portfolio_foundation_text_has_trade_or_execution_language("this is a research report")
    assert portfolio_foundation_text_has_trade_or_execution_language("kesin al")

def test_payload_safety():
    assert not portfolio_payload_has_forbidden_fields({"symbol": "AAPL"})
    assert portfolio_payload_has_forbidden_fields({"target_weight": 0.5})
