from usa_signal_bot.portfolio.risk_reporting.risk_budget_governance_report import (
    build_risk_budget_governance_report
)

def test_build_risk_budget_governance_report():
    report = build_risk_budget_governance_report({}, {})
    assert report.report_valid is True
    assert report.no_actual_target_weights is True
