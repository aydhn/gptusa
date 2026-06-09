from usa_signal_bot.portfolio.risk_reporting.constraint_governance_report import (
    build_constraint_governance_report
)

def test_build_constraint_governance_report():
    report = build_constraint_governance_report({})
    assert report.report_valid is True
    assert report.no_actual_target_weights is True
