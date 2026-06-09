from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_safety_boundary import (
    build_portfolio_risk_safety_boundary_rules,
    build_portfolio_risk_safety_boundary_result
)

def test_build_portfolio_risk_safety_boundary_result():
    rules = build_portfolio_risk_safety_boundary_rules()
    result = build_portfolio_risk_safety_boundary_result(rules)
    assert result.boundary_passed is True
    assert result.no_live_trading is True
    assert result.no_actual_target_weights is True
