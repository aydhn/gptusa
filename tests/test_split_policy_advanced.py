import pytest
from usa_signal_bot.ml_research.dataset_assembly.split_policy_builder import build_time_series_holdout_policy
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import MLSplitPolicyKind

def test_time_series_holdout_policy_valid_ratios():
    policy = build_time_series_holdout_policy(train_ratio=0.80, validation_ratio=0.10, test_ratio=0.10)
    assert len(policy.errors) == 0
    assert policy.policy_kind == MLSplitPolicyKind.TIME_SERIES_HOLDOUT
    assert policy.train_ratio == 0.80
    assert policy.time_ordered is True
    assert policy.leakage_safe_required is True

def test_time_series_holdout_policy_invalid_ratios():
    policy = build_time_series_holdout_policy(train_ratio=0.80, validation_ratio=0.50, test_ratio=0.10)
    assert len(policy.errors) > 0
    assert any("sum" in e.lower() for e in policy.errors)
