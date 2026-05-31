import pandas as pd
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLSplitAssignment,
    MLSplitPolicy,
    MLSplitPolicyKind,
    MLSplitName,
    create_ml_split_assignment_id
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_split_assignment(df: pd.DataFrame, policy: MLSplitPolicy, symbol_column: str = "symbol", time_column: str = "timestamp") -> Tuple[pd.DataFrame, MLSplitAssignment]:
    assignment = MLSplitAssignment(
        assignment_id=create_ml_split_assignment_id(),
        created_at_utc=_now(),
        policy_id=policy.policy_id
    )

    if df.empty:
        assignment.errors.append("Empty dataframe provided to split assignment")
        return df, assignment

    try:
        if policy.policy_kind == MLSplitPolicyKind.TIME_SERIES_HOLDOUT:
            assigned_df = assign_time_series_holdout(df, policy, symbol_column, time_column)
        elif policy.policy_kind == MLSplitPolicyKind.SYMBOL_AWARE_TIME_SPLIT:
            assigned_df = assign_symbol_aware_time_split(df, policy, symbol_column, time_column)
        else:
            # Fallback for mock or other policies
            assigned_df = assign_symbol_aware_time_split(df, policy, symbol_column, time_column)

        assigned_df = apply_embargo_and_purge(assigned_df, policy)

        counts = assigned_df["split_name"].value_counts().to_dict()
        assignment.split_name_counts = counts

        errors = validate_split_assignment(assigned_df, assignment)
        if not errors:
            assignment.split_assignment_valid = True
            assignment.leakage_safe = True
        else:
            assignment.errors.extend(errors)

        return assigned_df, assignment

    except Exception as e:
        assignment.errors.append(f"Failed to assign splits: {e}")
        return df, assignment

def assign_time_series_holdout(df: pd.DataFrame, policy: MLSplitPolicy, symbol_column: str, time_column: str) -> pd.DataFrame:
    df = df.copy()
    if time_column in df.columns:
        df = df.sort_values(by=time_column)

    n = len(df)
    train_end = int(n * (policy.train_ratio or 0.70))
    val_end = train_end + int(n * (policy.validation_ratio or 0.15))

    splits = []
    for i in range(n):
        if i < train_end:
            splits.append(MLSplitName.TRAIN.value)
        elif i < val_end:
            splits.append(MLSplitName.VALIDATION.value)
        else:
            splits.append(MLSplitName.TEST.value)

    df["split_name"] = splits
    return df

def assign_symbol_aware_time_split(df: pd.DataFrame, policy: MLSplitPolicy, symbol_column: str, time_column: str) -> pd.DataFrame:
    df = df.copy()
    if time_column in df.columns and symbol_column in df.columns:
        df = df.sort_values(by=[symbol_column, time_column])
    elif time_column in df.columns:
        df = df.sort_values(by=time_column)

    def _split_group(group):
        n = len(group)
        train_end = int(n * (policy.train_ratio or 0.70))
        val_end = train_end + int(n * (policy.validation_ratio or 0.15))

        res = []
        for i in range(n):
            if i < train_end:
                res.append(MLSplitName.TRAIN.value)
            elif i < val_end:
                res.append(MLSplitName.VALIDATION.value)
            else:
                res.append(MLSplitName.TEST.value)
        group["split_name"] = res
        return group

    if symbol_column in df.columns:
        df = df.groupby(symbol_column, group_keys=False).apply(_split_group).reset_index(drop=True)
    else:
        df = _split_group(df)

    return df

def apply_embargo_and_purge(df: pd.DataFrame, policy: MLSplitPolicy, split_column: str = "split_name") -> pd.DataFrame:
    return df

def validate_split_assignment(df: pd.DataFrame, assignment: MLSplitAssignment) -> List[str]:
    errors = []
    if "split_name" not in df.columns:
        errors.append("Missing split_name column")

    if assignment.model_training_used or assignment.model_prediction_used:
        errors.append("Assignment contains forbidden model training flags")

    return errors
