import pytest
from usa_signal_bot.portfolio_rebalance.walk_forward_adapter import (
    attach_rebalance_to_walk_forward_result, walk_forward_rebalance_summary,
    walk_forward_turnover_stability, walk_forward_rebalance_warnings
)
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceReview, RebalancePlan, TurnoverAssessment
from usa_signal_bot.core.enums import RebalanceReportType, RebalanceStatus, RebalanceMode, TurnoverStatus

def test_walk_forward_adapter():
    plan = RebalancePlan("p", "now", RebalanceMode.HYBRID, RebalanceStatus.PROPOSED, 1, 0, 0,
                         turnover_assessment=TurnoverAssessment("t", "now", 500, TurnoverStatus.EXCESSIVE, 1, 0))
    rev = RebalanceReview("r", "now", RebalanceReportType.FULL_REBALANCE_REVIEW, plan=plan)

    res = {"id": "1"}
    res = attach_rebalance_to_walk_forward_result(res, {"win1": rev})

    summ = walk_forward_rebalance_summary(res)
    assert summ["high_turnover_windows"] == 1

    stab = walk_forward_turnover_stability(res)
    assert stab["stability"] == "UNSTABLE"

    warns = walk_forward_rebalance_warnings(res)
    assert len(warns) == 1
    assert "unstable" in warns[0]
