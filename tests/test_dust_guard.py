import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus
from usa_signal_bot.portfolio_rebalance.dust_guard import (
    is_dust_rebalance_action, suppress_dust_rebalance_actions, dust_guard_summary
)

def build_actions():
    return [
        RebalanceAction("1", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED, delta_notional_usd=10.0),
        RebalanceAction("2", "MSFT", RebalanceActionType.DECREASE, RebalanceStatus.PROPOSED, delta_notional_usd=-500.0),
        RebalanceAction("3", "TSLA", RebalanceActionType.EXIT, RebalanceStatus.PROPOSED, delta_notional_usd=-5.0)
    ]

def test_is_dust_rebalance_action():
    actions = build_actions()
    assert is_dust_rebalance_action(actions[0], 25.0) is True
    assert is_dust_rebalance_action(actions[1], 25.0) is False

def test_suppress_dust_rebalance_actions():
    actions = build_actions()
    filtered = suppress_dust_rebalance_actions(actions, 25.0)

    aapl = next(a for a in filtered if a.symbol == "AAPL")
    assert aapl.status == RebalanceStatus.SUPPRESSED_BY_COST

    msft = next(a for a in filtered if a.symbol == "MSFT")
    assert msft.status == RebalanceStatus.PROPOSED

    tsla = next(a for a in filtered if a.symbol == "TSLA")
    assert tsla.status == RebalanceStatus.PROPOSED # exits are kept but warned
    assert any("Dust exit" in w for w in tsla.warnings)

def test_dust_guard_summary():
    actions = suppress_dust_rebalance_actions(build_actions(), 25.0)
    summary = dust_guard_summary(actions)
    assert summary["suppressed_count"] == 1
    assert summary["symbols"] == ["AAPL"]
