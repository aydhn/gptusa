import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, PortfolioPosition, DriftMeasurement
)
from usa_signal_bot.portfolio_rebalance.rebalance_planner import RebalancePlanner
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus, DriftType, DriftSeverity

def test_action_from_symbol_delta():
    planner = RebalancePlanner()
    curr = PortfolioPosition("1", "AAPL", 10, 1000)
    tgt = PortfolioPosition("2", "AAPL", 20, 2000)

    # Increase
    action = planner.action_from_symbol_delta("AAPL", curr, tgt)
    assert action.action_type == RebalanceActionType.INCREASE
    assert action.delta_notional_usd == 1000

    # Exit
    action = planner.action_from_symbol_delta("AAPL", curr, None)
    assert action.action_type == RebalanceActionType.EXIT
    assert action.delta_notional_usd == -1000

    # Enter
    action = planner.action_from_symbol_delta("MSFT", None, tgt)
    assert action.action_type == RebalanceActionType.ENTER
    assert action.delta_notional_usd == 2000

def test_propose_actions():
    planner = RebalancePlanner()
    current = CurrentPortfolioState("1", "now", 1000, 1000, [PortfolioPosition("1", "AAPL", 10, 1000)], 10000)
    target = TargetPortfolioState("2", "now", 2000, 2000, [PortfolioPosition("2", "AAPL", 20, 2000)], "src", 10000)

    drifts = [DriftMeasurement("d", "now", DriftType.SYMBOL_WEIGHT, "AAPL", DriftSeverity.HIGH, 1000, 2000, 10.0, 10.0)]
    actions = planner.propose_actions(current, target, drifts)
    assert len(actions) == 1
    assert actions[0].action_type == RebalanceActionType.INCREASE
    assert actions[0].status == RebalanceStatus.PROPOSED

def test_build_plan():
    planner = RebalancePlanner()
    current = CurrentPortfolioState("1", "now", 1000, 1000, [PortfolioPosition("1", "AAPL", 10, 1000)], 10000)
    target = TargetPortfolioState("2", "now", 2000, 2000, [PortfolioPosition("2", "AAPL", 20, 2000)], "src", 10000)

    plan = planner.build_plan(current, target)
    assert plan.proposed_action_count == 1
    assert plan.status == RebalanceStatus.PROPOSED
    assert plan.total_delta_notional_usd == 1000
    assert plan.turnover_assessment is not None
