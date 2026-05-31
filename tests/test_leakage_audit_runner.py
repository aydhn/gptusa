import pytest
import pandas as pd
from usa_signal_bot.ml_research.dataset_assembly.leakage_audit_runner import run_leakage_audit
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLSplitPolicy,
    MLSplitPolicyKind
)

def test_leakage_audit_detects_forbidden_columns():
    feature_df = pd.DataFrame({"symbol": ["AAPL"], "close": [100.0]})
    target_df = pd.DataFrame({"symbol": ["AAPL"], "buy_signal": [1]})
    label_df = pd.DataFrame({"symbol": ["AAPL"], "label": ["positive"]})
    split_df = pd.DataFrame({"symbol": ["AAPL"], "split_name": ["TRAIN"]})

    policy = MLSplitPolicy(
        policy_id="sp1", created_at_utc="now", policy_kind=MLSplitPolicyKind.SYMBOL_AWARE_TIME_SPLIT, policy_name="test"
    )

    res = run_leakage_audit(feature_df, target_df, label_df, split_df, policy)

    assert res.forbidden_output_detected is True
    assert res.leakage_audit_passed is False
    assert res.failed_rules > 0
