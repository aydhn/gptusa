from usa_signal_bot.portfolio.risk_reporting.portfolio_limitations_report import (
    build_portfolio_limitations_report
)

def test_build_portfolio_limitations_report():
    report = build_portfolio_limitations_report()
    assert report.report_valid is True
    assert "not an actual target weight" in str(report.notes)
