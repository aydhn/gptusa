import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus
from usa_signal_bot.portfolio_rebalance.turnover_cost import (
    estimate_action_turnover_cost, estimate_actions_turnover_cost,
    total_estimated_rebalance_cost_usd, total_estimated_rebalance_cost_bps
)

def build_actions():
    return [
        RebalanceAction("1", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED, delta_notional_usd=1000.0),
        RebalanceAction("2", "MSFT", RebalanceActionType.DECREASE, RebalanceStatus.PROPOSED, delta_notional_usd=-500.0)
    ]

def test_estimate_action_turnover_cost():
    action = build_actions()[0]
    action = estimate_action_turnover_cost(action)
    assert action.estimated_cost_bps == 50.0
    assert action.estimated_cost_usd == 1000 * (50 / 10000)

def test_estimate_actions_turnover_cost():
    actions = build_actions()
    cost_payloads = {
        "AAPL": {"adjusted_cost_bps": 100.0},
        "MSFT": {"adjusted_cost_bps": 20.0}
    }
    actions = estimate_actions_turnover_cost(actions, cost_payloads)

    assert actions[0].estimated_cost_bps == 100.0
    assert actions[0].estimated_cost_usd == 10.0

    assert actions[1].estimated_cost_bps == 20.0
    assert actions[1].estimated_cost_usd == 1.0

def test_total_estimated_rebalance_cost_usd():
    actions = estimate_actions_turnover_cost(build_actions())
    total_usd = total_estimated_rebalance_cost_usd(actions)
    # 1000 * 50bps = 5, 500 * 50bps = 2.5
    assert total_usd == 7.5

def test_total_estimated_rebalance_cost_bps():
    actions = estimate_actions_turnover_cost(build_actions())
    total_bps = total_estimated_rebalance_cost_bps(actions)
    assert total_bps == 50.0
