import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, PortfolioPosition
)
from usa_signal_bot.portfolio_rebalance.exposure_drift import (
    calculate_gross_exposure_drift, calculate_net_exposure_drift, calculate_long_short_exposure_drift
)

def test_gross_exposure_drift():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=5000, net_exposure_usd=3000,
        total_equity_usd=10000, positions=[]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=7000, target_net_exposure_usd=3000,
        total_equity_usd=10000, target_positions=[]
    )
    drift = calculate_gross_exposure_drift(current, target)
    assert drift.pct_drift == 20.0 # 70% - 50%

def test_net_exposure_drift():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=5000, net_exposure_usd=3000,
        total_equity_usd=10000, positions=[]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=5000, target_net_exposure_usd=1000,
        total_equity_usd=10000, target_positions=[]
    )
    drift = calculate_net_exposure_drift(current, target)
    assert drift.pct_drift == -20.0 # 10% - 30%

def test_long_short_exposure_drift():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=5000, net_exposure_usd=3000,
        total_equity_usd=10000, positions=[
            PortfolioPosition("1", "AAPL", 10, 4000, side="LONG"),
            PortfolioPosition("2", "TSLA", 10, 1000, side="SHORT")
        ]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=5000, target_net_exposure_usd=1000,
        total_equity_usd=10000, target_positions=[
            PortfolioPosition("3", "AAPL", 10, 3000, side="LONG"),
            PortfolioPosition("4", "TSLA", 10, 2000, side="SHORT")
        ]
    )
    drifts = calculate_long_short_exposure_drift(current, target)
    assert len(drifts) == 2
    long_drift = next(d for d in drifts if d.name == "Long Exposure")
    short_drift = next(d for d in drifts if d.name == "Short Exposure")

    assert long_drift.pct_drift == -10.0 # 30% - 40%
    assert short_drift.pct_drift == 10.0 # 20% - 10%
