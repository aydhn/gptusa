from usa_signal_bot.portfolio.risk_reporting.optimizer_objective_governance_report import (
    build_optimizer_objective_governance_report
)

def test_build_optimizer_objective_governance_report():
    report = build_optimizer_objective_governance_report({})
    assert report.report_valid is True
    assert report.no_actual_target_weights is True
    assert "best method denotes objective comparison diagnostic only" in report.notes[0]
