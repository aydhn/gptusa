from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLSplitPolicy,
    MLSplitPolicyKind,
    create_ml_split_policy_id
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_default_split_policy(policy_kind: MLSplitPolicyKind = MLSplitPolicyKind.SYMBOL_AWARE_TIME_SPLIT) -> MLSplitPolicy:
    if policy_kind == MLSplitPolicyKind.WALK_FORWARD:
        return build_walk_forward_split_policy()
    return build_time_series_holdout_policy()

def build_time_series_holdout_policy(
    train_ratio: float = 0.70,
    validation_ratio: float = 0.15,
    test_ratio: float = 0.15,
    embargo_bars: int = 5,
    purge_bars: int = 5
) -> MLSplitPolicy:
    policy = MLSplitPolicy(
        policy_id=create_ml_split_policy_id(),
        created_at_utc=_now(),
        policy_kind=MLSplitPolicyKind.TIME_SERIES_HOLDOUT,
        policy_name="default_time_series_holdout",
        train_ratio=train_ratio,
        validation_ratio=validation_ratio,
        test_ratio=test_ratio,
        embargo_bars=embargo_bars,
        purge_bars=purge_bars,
        symbol_aware=True,
        time_ordered=True,
        leakage_safe_required=True
    )
    policy.errors.extend(validate_split_policy(policy))
    return policy

def build_walk_forward_split_policy(
    window_bars: int = 252,
    step_bars: int = 21,
    min_train_bars: int = 252,
    embargo_bars: int = 5,
    purge_bars: int = 5
) -> MLSplitPolicy:
    policy = MLSplitPolicy(
        policy_id=create_ml_split_policy_id(),
        created_at_utc=_now(),
        policy_kind=MLSplitPolicyKind.WALK_FORWARD,
        policy_name="default_walk_forward",
        walk_forward_window_bars=window_bars,
        walk_forward_step_bars=step_bars,
        min_train_bars=min_train_bars,
        embargo_bars=embargo_bars,
        purge_bars=purge_bars,
        symbol_aware=True,
        time_ordered=True,
        leakage_safe_required=True
    )
    policy.errors.extend(validate_split_policy(policy))
    return policy

def validate_split_policy(policy: MLSplitPolicy) -> List[str]:
    errors = []
    if not policy.time_ordered:
        errors.append("Policy must be time_ordered")
    if not policy.leakage_safe_required:
        errors.append("Policy must have leakage_safe_required=True")

    if policy.policy_kind in [MLSplitPolicyKind.TIME_SERIES_HOLDOUT, MLSplitPolicyKind.SYMBOL_AWARE_TIME_SPLIT]:
        if policy.train_ratio is None or policy.validation_ratio is None or policy.test_ratio is None:
            errors.append("Holdout policies require train/validation/test ratios")
        else:
            total = policy.train_ratio + policy.validation_ratio + policy.test_ratio
            if abs(total - 1.0) > 1e-5:
                errors.append(f"Ratios must sum to 1.0, got {total}")

    if policy.policy_kind == MLSplitPolicyKind.WALK_FORWARD:
        if policy.walk_forward_window_bars is None or policy.walk_forward_step_bars is None:
            errors.append("Walk forward policies require window and step bars")

    if policy.produces_trade_signal or policy.produces_order_decision:
        errors.append("Policy contains forbidden semantic flags")

    return errors

def split_policy_summary(policy: MLSplitPolicy) -> Dict[str, Any]:
    return {
        "policy_id": policy.policy_id,
        "policy_kind": policy.policy_kind.value,
        "valid": len(policy.errors) == 0,
        "errors": policy.errors
    }

def split_policy_to_text(policy: MLSplitPolicy, limit: int = 300) -> str:
    s = json.dumps(split_policy_summary(policy), indent=2)
    if len(s) > limit:
        return s[:limit] + "..."
    return s
