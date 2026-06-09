from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_validation import (
    validate_portfolio_risk_context_report,
    validate_no_execution_language_in_portfolio_risk_text
)
from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_report import build_portfolio_risk_context

def test_validate_portfolio_risk_context_report():
    context = build_portfolio_risk_context()
    report = validate_portfolio_risk_context_report(context)
    assert report.valid is True
    assert report.error_count == 0

def test_validate_no_execution_language_in_portfolio_risk_text():
    report = validate_no_execution_language_in_portfolio_risk_text("buy this stock now")
    assert report.valid is False
    assert report.error_count == 1
