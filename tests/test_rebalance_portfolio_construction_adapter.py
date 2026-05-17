import pytest
from usa_signal_bot.portfolio_rebalance.portfolio_construction_adapter import (
    rebalance_target_from_portfolio_construction_plan,
    attach_rebalance_feedback_to_construction_plan,
    construction_rebalance_summary
)
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalancePlan
from usa_signal_bot.core.enums import RebalanceMode, RebalanceStatus

def test_portfolio_construction_adapter():
    plan_payload = {
        "plan_id": "p1",
        "capital_state": {"total_equity_usd": 10000},
        "final_allocations": [{"symbol": "AAPL", "target_notional_usd": 1000}]
    }

    tgt = rebalance_target_from_portfolio_construction_plan(plan_payload)
    assert tgt.total_equity_usd == 10000
    assert len(tgt.target_positions) == 1
    assert tgt.target_positions[0].symbol == "AAPL"

    rb_plan = RebalancePlan("rp1", "now", RebalanceMode.HYBRID, RebalanceStatus.PROPOSED, 1, 0, 0)
    updated_payload = attach_rebalance_feedback_to_construction_plan(plan_payload, rb_plan)

    assert "rebalance_feedback" in updated_payload
    summ = construction_rebalance_summary(updated_payload)
    assert summ["status"] == "PROPOSED"
    assert summ["proposed_action_count"] == 1
