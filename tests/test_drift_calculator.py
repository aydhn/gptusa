import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, PortfolioPosition
)
from usa_signal_bot.portfolio_rebalance.drift_calculator import (
    calculate_symbol_drift, classify_drift_severity, aggregate_drift_score
)
from usa_signal_bot.core.enums import DriftSeverity

def test_classify_drift_severity():
    assert classify_drift_severity(0.5) == DriftSeverity.NONE
    assert classify_drift_severity(2.0) == DriftSeverity.LOW
    assert classify_drift_severity(4.0) == DriftSeverity.MODERATE
    assert classify_drift_severity(8.0) == DriftSeverity.HIGH
    assert classify_drift_severity(12.0) == DriftSeverity.CRITICAL
    assert classify_drift_severity(None) == DriftSeverity.INSUFFICIENT_DATA

def test_calculate_symbol_drift_equal():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=1000, net_exposure_usd=1000,
        total_equity_usd=10000, positions=[
            PortfolioPosition(position_id="1", symbol="AAPL", quantity=10, market_value_usd=1000)
        ]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=1000, target_net_exposure_usd=1000,
        total_equity_usd=10000, target_positions=[
            PortfolioPosition(position_id="2", symbol="AAPL", quantity=10, market_value_usd=1000)
        ]
    )
    drifts = calculate_symbol_drift(current, target)
    assert len(drifts) == 1
    assert drifts[0].absolute_drift == 0.0
    assert drifts[0].severity == DriftSeverity.NONE

def test_calculate_symbol_drift_increase():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=1000, net_exposure_usd=1000,
        total_equity_usd=10000, positions=[
            PortfolioPosition(position_id="1", symbol="AAPL", quantity=10, market_value_usd=1000)
        ]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=2000, target_net_exposure_usd=2000,
        total_equity_usd=10000, target_positions=[
            PortfolioPosition(position_id="2", symbol="AAPL", quantity=20, market_value_usd=2000)
        ]
    )
    drifts = calculate_symbol_drift(current, target)
    assert len(drifts) == 1
    assert drifts[0].pct_drift == 10.0 # 20% - 10%
    assert drifts[0].absolute_drift == 10.0

def test_calculate_symbol_drift_decrease():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=2000, net_exposure_usd=2000,
        total_equity_usd=10000, positions=[
            PortfolioPosition(position_id="1", symbol="AAPL", quantity=20, market_value_usd=2000)
        ]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=1000, target_net_exposure_usd=1000,
        total_equity_usd=10000, target_positions=[
            PortfolioPosition(position_id="2", symbol="AAPL", quantity=10, market_value_usd=1000)
        ]
    )
    drifts = calculate_symbol_drift(current, target)
    assert len(drifts) == 1
    assert drifts[0].pct_drift == -10.0 # 10% - 20%
    assert drifts[0].absolute_drift == 10.0

def test_calculate_symbol_drift_exit():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=1000, net_exposure_usd=1000,
        total_equity_usd=10000, positions=[
            PortfolioPosition(position_id="1", symbol="AAPL", quantity=10, market_value_usd=1000)
        ]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=0, target_net_exposure_usd=0,
        total_equity_usd=10000, target_positions=[]
    )
    drifts = calculate_symbol_drift(current, target)
    assert len(drifts) == 1
    assert drifts[0].name == "AAPL"
    assert drifts[0].pct_drift == -10.0

def test_calculate_symbol_drift_enter():
    current = CurrentPortfolioState(
        state_id="1", created_at_utc="now", gross_exposure_usd=0, net_exposure_usd=0,
        total_equity_usd=10000, positions=[]
    )
    target = TargetPortfolioState(
        target_id="2", created_at_utc="now", target_gross_exposure_usd=1000, target_net_exposure_usd=1000,
        total_equity_usd=10000, target_positions=[
            PortfolioPosition(position_id="2", symbol="AAPL", quantity=10, market_value_usd=1000)
        ]
    )
    drifts = calculate_symbol_drift(current, target)
    assert len(drifts) == 1
    assert drifts[0].name == "AAPL"
    assert drifts[0].pct_drift == 10.0

def test_aggregate_drift_score():
    drifts = calculate_symbol_drift(
        CurrentPortfolioState("1", "now", 0, 0, [], 10000, 10000, [], [], {}),
        TargetPortfolioState("2", "now", 1000, 1000, [
            PortfolioPosition("3", "AAPL", 10, 1000)
        ], "plan", 10000, [], [], {})
    )
    score = aggregate_drift_score(drifts)
    assert score == 10.0
