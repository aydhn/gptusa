import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus
from usa_signal_bot.portfolio_rebalance.drawdown_rebalance_throttle import (
    should_throttle_rebalance_for_drawdown, apply_drawdown_rebalance_throttle
)

def build_actions():
    return [
        RebalanceAction("1", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED),
        RebalanceAction("2", "MSFT", RebalanceActionType.ENTER, RebalanceStatus.PROPOSED),
        RebalanceAction("3", "TSLA", RebalanceActionType.EXIT, RebalanceStatus.PROPOSED)
    ]

def test_should_throttle():
    assert should_throttle_rebalance_for_drawdown(None) is False
    assert should_throttle_rebalance_for_drawdown(5.0) is False
    assert should_throttle_rebalance_for_drawdown(8.0) is True

def test_apply_drawdown_throttle():
    actions = build_actions()

    # Moderate drawdown - enters are blocked
    filtered_11 = apply_drawdown_rebalance_throttle(actions.copy(), 11.0)
    assert filtered_11[0].status == RebalanceStatus.PROPOSED
    assert filtered_11[1].status == RebalanceStatus.SUPPRESSED_BY_DRAWDOWN
    assert filtered_11[2].status == RebalanceStatus.PROPOSED

    # Critical drawdown - all increases blocked
    actions2 = build_actions()
    filtered_16 = apply_drawdown_rebalance_throttle(actions2, 16.0)
    assert filtered_16[0].status == RebalanceStatus.SUPPRESSED_BY_DRAWDOWN
    assert filtered_16[1].status == RebalanceStatus.SUPPRESSED_BY_DRAWDOWN
    assert filtered_16[2].status == RebalanceStatus.PROPOSED # exit allowed
