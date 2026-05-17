import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_thresholds import (
    default_rebalance_threshold_policy, build_rebalance_threshold_policy_from_config,
    adjust_threshold_policy_for_cost, adjust_threshold_policy_for_regime,
    adjust_threshold_policy_for_drawdown
)

def test_default_policy():
    policy = default_rebalance_threshold_policy()
    assert policy.min_symbol_drift_pct == 1.0
    assert policy.max_turnover_pct_equity == 10.0

def test_build_from_config():
    cfg = {"min_symbol_drift_pct": 2.0}
    policy = build_rebalance_threshold_policy_from_config(cfg)
    assert policy.min_symbol_drift_pct == 2.0
    assert policy.min_trade_notional_usd == 25.0 # default

def test_adjust_for_cost():
    policy = default_rebalance_threshold_policy()
    cost_payload = {"status": "HIGH"}
    adj_policy = adjust_threshold_policy_for_cost(policy, cost_payload)
    assert adj_policy.min_symbol_drift_pct == 1.5
    assert adj_policy.max_turnover_pct_equity == (10.0 / 1.5)

def test_adjust_for_regime():
    policy = default_rebalance_threshold_policy()
    regime_payload = {"transition_risk": "HIGH"}
    adj_policy = adjust_threshold_policy_for_regime(policy, regime_payload)
    assert adj_policy.min_symbol_drift_pct == 1.5

def test_adjust_for_drawdown():
    policy = default_rebalance_threshold_policy()
    adj_policy = adjust_threshold_policy_for_drawdown(policy, drawdown_pct=8.0)
    assert adj_policy.min_symbol_drift_pct == 2.0
