import pytest
from usa_signal_bot.portfolio_rebalance.backtest_adapter import (
    attach_rebalance_to_backtest_result, simulate_rebalance_metadata_for_backtest_window,
    backtest_rebalance_summary, backtest_turnover_warnings
)
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceReview, RebalancePlan, TurnoverAssessment
from usa_signal_bot.core.enums import RebalanceReportType, RebalanceStatus, RebalanceMode, TurnoverStatus

def test_backtest_adapter():
    plan = RebalancePlan("p", "now", RebalanceMode.HYBRID, RebalanceStatus.PROPOSED, 1, 0, 0,
                         turnover_assessment=TurnoverAssessment("t", "now", 500, TurnoverStatus.EXCESSIVE, 1, 0))
    rev = RebalanceReview("r", "now", RebalanceReportType.FULL_REBALANCE_REVIEW, plan=plan)

    res = {"id": "1"}
    res = attach_rebalance_to_backtest_result(res, rev)
    assert "rebalance_metadata" in res

    win = simulate_rebalance_metadata_for_backtest_window({"window_id": "1"})
    assert win["rebalance_simulation_available"] is True

    summ = backtest_rebalance_summary(res)
    assert summ["plan_status"] == "PROPOSED"

    warns = backtest_turnover_warnings(res)
    assert len(warns) == 1
    assert "EXCESSIVE" in warns[0]
