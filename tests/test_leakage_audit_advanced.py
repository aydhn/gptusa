import pytest
import pandas as pd
from usa_signal_bot.ml_research.dataset_assembly.leakage_audit_runner import run_leakage_audit
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLSplitPolicy,
    MLSplitPolicyKind,
    MLSplitName
)

def test_leakage_audit_detects_no_leakage_in_safe_scenario():
    # Feature
    feature_df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "price": [100.0, 101.0, 102.0]
    })

    # Target
    target_df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "target_fwd_return_1": [0.01, 0.009, 0.0]
    })

    # Label
    label_df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "label_return_class": ["positive_return_bucket", "neutral_return_bucket", "neutral_return_bucket"]
    })

    # Split
    split_df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "split_name": [MLSplitName.TRAIN.value, MLSplitName.VALIDATION.value, MLSplitName.TEST.value]
    })

    policy = MLSplitPolicy(
        policy_id="sp1", created_at_utc="now", policy_kind=MLSplitPolicyKind.SYMBOL_AWARE_TIME_SPLIT, policy_name="test"
    )

    res = run_leakage_audit(feature_df, target_df, label_df, split_df, policy)

    # Since our simple audit defaults to PASS for structure tests and passes forbidden output tests
    assert res.leakage_audit_passed is True
    assert res.forbidden_output_detected is False

def test_leakage_audit_detects_trade_signals():
    feature_df = pd.DataFrame({
        "symbol": ["AAPL"],
        "timestamp": ["2023-01-01"],
        "buy": [1.0] # forbidden
    })

    target_df = pd.DataFrame({
        "symbol": ["AAPL"],
        "timestamp": ["2023-01-01"],
        "target_fwd_return_1": [0.01]
    })

    label_df = pd.DataFrame({
        "symbol": ["AAPL"],
        "timestamp": ["2023-01-01"],
        "label_return_class": ["positive_return_bucket"]
    })

    split_df = pd.DataFrame({
        "symbol": ["AAPL"],
        "timestamp": ["2023-01-01"],
        "split_name": [MLSplitName.TRAIN.value]
    })

    policy = MLSplitPolicy(
        policy_id="sp1", created_at_utc="now", policy_kind=MLSplitPolicyKind.SYMBOL_AWARE_TIME_SPLIT, policy_name="test"
    )

    res = run_leakage_audit(feature_df, target_df, label_df, split_df, policy)

    assert res.leakage_audit_passed is False
    assert res.forbidden_output_detected is True
