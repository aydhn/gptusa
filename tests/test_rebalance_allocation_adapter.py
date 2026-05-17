import pytest
from usa_signal_bot.portfolio_rebalance.allocation_adapter import (
    current_state_from_allocation_payloads,
    rebalance_actions_to_allocation_adjustments,
    attach_rebalance_to_allocation_review
)
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction, RebalancePlan
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus, RebalanceMode

def test_allocation_adapter():
    payloads = [{"symbol": "AAPL", "final_size_usd": 1000, "side": "LONG"}]
    curr = current_state_from_allocation_payloads(payloads, 10000)
    assert curr.gross_exposure_usd == 1000
    assert len(curr.positions) == 1

    act = RebalanceAction("1", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED, delta_notional_usd=500)
    adjs = rebalance_actions_to_allocation_adjustments([act])
    assert len(adjs) == 1
    assert adjs[0]["action_type"] == "INCREASE"
    assert adjs[0]["delta_notional_usd"] == 500

    plan = RebalancePlan("rp1", "now", RebalanceMode.HYBRID, RebalanceStatus.PROPOSED, 1, 0, 0)
    review = {"review_id": "r1"}
    updated_review = attach_rebalance_to_allocation_review(review, plan)
    assert "rebalance_metadata" in updated_review
