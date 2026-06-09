from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_summary import (
    build_portfolio_risk_summary, validate_portfolio_risk_summary
)

def test_build_portfolio_risk_summary():
    summary = build_portfolio_risk_summary([])
    assert summary.method_count == 0
    assert summary.summary_valid is True

def test_validate_portfolio_risk_summary():
    summary = build_portfolio_risk_summary([])
    summary.actual_target_weight_detected = True
    errs = validate_portfolio_risk_summary(summary)
    assert "actual_target_weight_detected" in errs
