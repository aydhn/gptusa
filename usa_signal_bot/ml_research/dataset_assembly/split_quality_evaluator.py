import pandas as pd
from typing import Any, Dict, List
from datetime import datetime, timezone
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLSplitQualityProfile, MLDatasetQualityStatus, MLSplitAssignment, MLSplitPolicy, MLSplitName, create_ml_split_quality_profile_id
)

def _now() -> str: return datetime.now(timezone.utc).isoformat()

def build_split_quality_profile(split_df: pd.DataFrame, assignment: MLSplitAssignment, policy: MLSplitPolicy) -> MLSplitQualityProfile:
    counts = assignment.split_name_counts
    p = MLSplitQualityProfile(
        profile_id=create_ml_split_quality_profile_id(), created_at_utc=_now(), policy_id=policy.policy_id,
        status=MLDatasetQualityStatus.ACCEPTABLE, score=100.0,
        train_count=counts.get(MLSplitName.TRAIN.value, 0), validation_count=counts.get(MLSplitName.VALIDATION.value, 0),
        test_count=counts.get(MLSplitName.TEST.value, 0), embargo_count=counts.get(MLSplitName.EMBARGO.value, 0), purged_count=counts.get(MLSplitName.PURGED.value, 0)
    )
    p.score = compute_split_balance_score(split_df)
    p.score = min(p.score, compute_split_leakage_safety_score(assignment))
    if p.score < 50.0: p.status = MLDatasetQualityStatus.LOW
    elif p.score < 80.0: p.status = MLDatasetQualityStatus.WARNING
    p.errors.extend(validate_split_quality_profile(p))
    return p

def compute_split_balance_score(split_df: pd.DataFrame, split_column: str = "split_name") -> float:
    if split_df.empty or split_column not in split_df.columns: return 0.0
    train_c = len(split_df[split_df[split_column] == MLSplitName.TRAIN.value])
    val_c = len(split_df[split_df[split_column] == MLSplitName.VALIDATION.value])
    test_c = len(split_df[split_df[split_column] == MLSplitName.TEST.value])
    if train_c == 0: return 0.0
    if val_c == 0 and test_c == 0: return 50.0
    return 100.0

def compute_split_leakage_safety_score(assignment: MLSplitAssignment) -> float:
    return 100.0 if assignment.leakage_safe else 0.0

def validate_split_quality_profile(profile: MLSplitQualityProfile) -> List[str]:
    return ["Profile contains forbidden semantic flags"] if profile.produces_trade_signal or profile.investment_advice else []

def split_quality_summary(profile: MLSplitQualityProfile) -> Dict[str, Any]:
    return {"profile_id": profile.profile_id, "status": profile.status.value, "score": profile.score, "train_count": profile.train_count, "validation_count": profile.validation_count, "test_count": profile.test_count}

def split_quality_to_text(profile: MLSplitQualityProfile, limit: int = 300) -> str:
    s = json.dumps(split_quality_summary(profile), indent=2)
    return s[:limit] + "..." if len(s) > limit else s
