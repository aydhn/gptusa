import pytest
import pandas as pd
from usa_signal_bot.ml_research.dataset_assembly.split_assignment_builder import build_split_assignment
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLSplitPolicy,
    MLSplitPolicyKind,
    MLSplitName
)

def test_split_assignment_does_not_shuffle_in_time_series():
    df = pd.DataFrame({
        "symbol": ["AAPL"] * 10,
        "timestamp": [f"2023-01-{i:02d}" for i in range(1, 11)],
        "price": [100.0 + i for i in range(10)]
    })

    # Intentionally shuffle the df to ensure the builder sorts it back
    df = df.sample(frac=1.0, random_state=42)

    policy = MLSplitPolicy(
        policy_id="sp1", created_at_utc="now", policy_kind=MLSplitPolicyKind.TIME_SERIES_HOLDOUT,
        policy_name="test", train_ratio=0.7, validation_ratio=0.15, test_ratio=0.15
    )

    assigned_df, assignment = build_split_assignment(df, policy)

    assert assignment.split_assignment_valid is True

    # Since it's time series, it must have sorted by timestamp
    assert assigned_df["timestamp"].is_monotonic_increasing is True

    # First 7 should be TRAIN
    assert (assigned_df.iloc[:7]["split_name"] == MLSplitName.TRAIN.value).all()
    # Next 1 should be VALIDATION (int(10*0.15) = 1)
    assert (assigned_df.iloc[7:8]["split_name"] == MLSplitName.VALIDATION.value).all()
    # Last 2 should be TEST
    assert (assigned_df.iloc[8:]["split_name"] == MLSplitName.TEST.value).all()
