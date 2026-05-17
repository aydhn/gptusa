import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, PortfolioPosition
)
from usa_signal_bot.portfolio_rebalance.bucket_drift import (
    calculate_sector_cluster_drift, calculate_strategy_regime_drift, calculate_liquidity_cost_bucket_drift
)

def build_test_states():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=1000, net_exposure_usd=1000,
        total_equity_usd=10000, positions=[
            PortfolioPosition("1", "AAPL", 10, 1000, sector="Tech", cluster="Growth",
                              strategy_name="Trend", regime_label="RiskOn",
                              liquidity_bucket="Deep", cost_bucket="Low")
        ]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=2000, target_net_exposure_usd=2000,
        total_equity_usd=10000, target_positions=[
            PortfolioPosition("2", "AAPL", 10, 1000, sector="Tech", cluster="Growth",
                              strategy_name="Trend", regime_label="RiskOn",
                              liquidity_bucket="Deep", cost_bucket="Low"),
            PortfolioPosition("3", "MSFT", 10, 1000, sector="Tech", cluster="Growth",
                              strategy_name="Momentum", regime_label="RiskOn",
                              liquidity_bucket="Normal", cost_bucket="High")
        ]
    )
    return current, target

def test_sector_cluster_drift():
    current, target = build_test_states()
    drifts = calculate_sector_cluster_drift(current, target)
    assert any(d.name == "SECTOR_WEIGHT_Tech" for d in drifts)
    tech_drift = next(d for d in drifts if d.name == "SECTOR_WEIGHT_Tech")
    assert tech_drift.pct_drift == 10.0 # 20% - 10%

def test_strategy_regime_drift():
    current, target = build_test_states()
    drifts = calculate_strategy_regime_drift(current, target)
    momentum_drift = next(d for d in drifts if d.name == "STRATEGY_WEIGHT_Momentum")
    assert momentum_drift.pct_drift == 10.0 # 10% - 0%

def test_liquidity_cost_bucket_drift():
    current, target = build_test_states()
    drifts = calculate_liquidity_cost_bucket_drift(current, target)
    high_cost_drift = next(d for d in drifts if d.name == "COST_BUCKET_WEIGHT_High")
    assert high_cost_drift.pct_drift == 10.0 # 10% - 0%
