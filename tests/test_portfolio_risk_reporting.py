from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_reporting import (
    portfolio_risk_limitations_text
)

def test_portfolio_risk_limitations_text():
    text = portfolio_risk_limitations_text()
    assert "Research only" in text
