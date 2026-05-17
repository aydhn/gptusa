import pytest
from usa_signal_bot.portfolio_rebalance.paper_adapter import (
    build_current_state_from_paper_store_payload, attach_rebalance_plan_to_paper_state,
    paper_rebalance_actions_as_local_intents, paper_rebalance_allowed, paper_rebalance_summary
)
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalancePlan, RebalanceAction
from usa_signal_bot.core.enums import RebalanceMode, RebalanceStatus, RebalanceActionType

def test_paper_adapter():
    payload = {
        "total_equity_usd": 10000,
        "cash_usd": 10000,
        "positions": []
    }
    state = build_current_state_from_paper_store_payload(payload)
    assert state.total_equity_usd == 10000

    plan = RebalancePlan("p", "now", RebalanceMode.HYBRID, RebalanceStatus.PROPOSED, 1, 0, 0,
                         actions=[
                             RebalanceAction("a", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED, delta_notional_usd=500),
                             RebalanceAction("b", "MSFT", RebalanceActionType.INCREASE, RebalanceStatus.SUPPRESSED_BY_COST, delta_notional_usd=500)
                         ])

    st = attach_rebalance_plan_to_paper_state(payload, plan)
    assert "rebalance_metadata" in st

    intents = paper_rebalance_actions_as_local_intents(plan)
    assert len(intents) == 1
    assert intents[0]["symbol"] == "AAPL"

    assert paper_rebalance_allowed(plan.actions[0]) is True
    assert paper_rebalance_allowed(plan.actions[1]) is False

    summ = paper_rebalance_summary(st)
    assert summ["plan_id"] == "p"
