import pytest
from usa_signal_bot.portfolio_rebalance.risk_adapter import (
    rebalance_risk_summary, rebalance_risk_warnings, attach_rebalance_to_risk_report
)
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalancePlan, DriftMeasurement, TurnoverAssessment
from usa_signal_bot.core.enums import RebalanceMode, RebalanceStatus, DriftType, DriftSeverity, TurnoverStatus

def test_risk_adapter():
    drift = DriftMeasurement("d1", "now", DriftType.SYMBOL_WEIGHT, "AAPL", DriftSeverity.CRITICAL)
    ta = TurnoverAssessment("t1", "now", 5000, TurnoverStatus.EXCESSIVE, 1, 0, estimated_turnover_pct_equity=25.0)
    plan = RebalancePlan("rp1", "now", RebalanceMode.HYBRID, RebalanceStatus.PROPOSED, 1, 0, 1, drift_measurements=[drift], turnover_assessment=ta)

    summ = rebalance_risk_summary(plan)
    assert summ["high_drift_count"] == 1
    assert summ["turnover_pct"] == 25.0
    assert summ["blocked_action_count"] == 1

    warns = rebalance_risk_warnings(plan)
    assert len(warns) == 3 # turnover, critical drift, blocked actions

    report = {"report_id": "rep1"}
    report = attach_rebalance_to_risk_report(report, plan)
    assert "rebalance_metadata" in report
    assert "rebalance_risk_summary" in report
    assert "rebalance_risk_warnings" in report
