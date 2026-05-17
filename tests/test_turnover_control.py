import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus, TurnoverStatus
from usa_signal_bot.portfolio_rebalance.turnover_control import (
    estimate_rebalance_turnover_usd, estimate_rebalance_turnover_pct_equity,
    classify_turnover_status, assess_turnover, suppress_actions_to_fit_turnover
)

def build_actions():
    return [
        RebalanceAction("1", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED, delta_notional_usd=1000.0),
        RebalanceAction("2", "MSFT", RebalanceActionType.DECREASE, RebalanceStatus.PROPOSED, delta_notional_usd=-500.0),
        RebalanceAction("3", "TSLA", RebalanceActionType.EXIT, RebalanceStatus.PROPOSED, delta_notional_usd=-2000.0)
    ]

def test_estimate_rebalance_turnover_usd():
    actions = build_actions()
    turnover = estimate_rebalance_turnover_usd(actions)
    assert turnover == 3500.0

def test_estimate_rebalance_turnover_pct_equity():
    pct = estimate_rebalance_turnover_pct_equity(3500.0, 10000.0)
    assert pct == 35.0

def test_classify_turnover_status():
    assert classify_turnover_status(5.0, 10.0) == TurnoverStatus.ACCEPTABLE
    assert classify_turnover_status(8.0, 10.0) == TurnoverStatus.WARNING
    assert classify_turnover_status(15.0, 10.0) == TurnoverStatus.HIGH
    assert classify_turnover_status(25.0, 10.0) == TurnoverStatus.EXCESSIVE

def test_assess_turnover():
    actions = build_actions()
    assessment = assess_turnover(actions, total_equity_usd=10000.0, max_turnover_pct_equity=10.0)
    assert assessment.estimated_turnover_usd == 3500.0
    assert assessment.estimated_turnover_pct_equity == 35.0
    assert assessment.status == TurnoverStatus.EXCESSIVE

def test_suppress_actions_to_fit_turnover():
    actions = build_actions()
    # Turnover is 3500. Limit is 20% of 10000 = 2000.
    # Exits are prioritized, so TSLA (-2000) should be kept.
    # AAPL and MSFT should be suppressed.
    filtered = suppress_actions_to_fit_turnover(actions, total_equity_usd=10000.0, max_turnover_pct_equity=20.0)

    aapl = next(a for a in filtered if a.symbol == "AAPL")
    msft = next(a for a in filtered if a.symbol == "MSFT")
    tsla = next(a for a in filtered if a.symbol == "TSLA")

    assert tsla.status == RebalanceStatus.PROPOSED
    assert aapl.status == RebalanceStatus.REDUCED_BY_TURNOVER
    assert msft.status == RebalanceStatus.REDUCED_BY_TURNOVER
