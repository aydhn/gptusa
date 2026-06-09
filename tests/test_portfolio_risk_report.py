from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_report import (
    build_portfolio_risk_context, build_portfolio_risk_full_review
)

def test_build_portfolio_risk_full_review():
    review = build_portfolio_risk_full_review()
    assert review.context.produces_live_signal is False
    assert review.context.actual_target_weights_produced is False
