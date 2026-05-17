import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus
from usa_signal_bot.portfolio_rebalance.regime_rebalance_throttle import (
    should_throttle_rebalance_for_regime, apply_regime_rebalance_throttle
)

def build_actions():
    return [
        RebalanceAction("1", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED),
        RebalanceAction("2", "MSFT", RebalanceActionType.DECREASE, RebalanceStatus.PROPOSED)
    ]

def test_should_throttle():
    assert should_throttle_rebalance_for_regime() is False
    assert should_throttle_rebalance_for_regime(transition_payload={"risk": "HIGH"}) is True
    assert should_throttle_rebalance_for_regime(regime_payload={"breadth": "RISK_OFF"}) is True

def test_apply_throttle():
    actions = build_actions()
    transition = {"risk": "HIGH"}

    filtered = apply_regime_rebalance_throttle(actions, transition_payload=transition)

    # Increase is suppressed
    assert filtered[0].status == RebalanceStatus.SUPPRESSED_BY_REGIME
    # Decrease is allowed
    assert filtered[1].status == RebalanceStatus.PROPOSED
