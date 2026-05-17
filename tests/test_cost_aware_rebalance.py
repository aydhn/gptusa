import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus
from usa_signal_bot.portfolio_rebalance.cost_aware_rebalance import (
    should_suppress_rebalance_for_cost, apply_cost_aware_rebalance_filter
)

def build_actions():
    return [
        RebalanceAction("1", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED),
        RebalanceAction("2", "MSFT", RebalanceActionType.DECREASE, RebalanceStatus.PROPOSED),
        RebalanceAction("3", "TSLA", RebalanceActionType.ENTER, RebalanceStatus.PROPOSED, estimated_cost_bps=350.0)
    ]

def test_should_suppress_rebalance_for_cost():
    a = build_actions()[0]
    assert should_suppress_rebalance_for_cost(a, None) is False
    assert should_suppress_rebalance_for_cost(a, {"status": "EXCESSIVE"}) is True
    assert should_suppress_rebalance_for_cost(a, {"market_impact_severity": "CRITICAL"}) is True
    assert should_suppress_rebalance_for_cost(a, {"cost_robustness_status": "FAILED"}) is True

    # Exits are not suppressed
    exit_action = build_actions()[1]
    assert should_suppress_rebalance_for_cost(exit_action, {"status": "EXCESSIVE"}) is False

def test_apply_cost_aware_rebalance_filter():
    actions = build_actions()
    payloads = {"AAPL": {"status": "EXCESSIVE"}}

    filtered = apply_cost_aware_rebalance_filter(actions, payloads)

    assert filtered[0].status == RebalanceStatus.SUPPRESSED_BY_COST
    assert filtered[1].status == RebalanceStatus.PROPOSED # decrease not suppressed
    assert filtered[2].status == RebalanceStatus.SUPPRESSED_BY_COST # TSLA has high bps
