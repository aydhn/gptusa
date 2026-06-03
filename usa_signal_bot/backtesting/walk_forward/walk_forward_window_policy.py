from typing import Any, Dict, List

from usa_signal_bot.core.enums import WalkForwardWindowKind, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardWindowPolicy,
    create_walk_forward_window_policy_id,
    _now_utc
)

def build_default_walk_forward_window_policy() -> WalkForwardWindowPolicy:
    return build_custom_walk_forward_window_policy(
        min_train_periods=60,
        oos_periods=20,
        step_periods=20,
        max_folds=10,
        anchored_enabled=True,
        rolling_enabled=True
    )

def build_custom_walk_forward_window_policy(
    min_train_periods: int,
    oos_periods: int,
    step_periods: int,
    max_folds: int,
    anchored_enabled: bool = True,
    rolling_enabled: bool = True
) -> WalkForwardWindowPolicy:
    policy = WalkForwardWindowPolicy(
        policy_id=create_walk_forward_window_policy_id(),
        created_at_utc=_now_utc(),
        policy_name="Custom Window Policy",
        min_train_periods=min_train_periods,
        oos_periods=oos_periods,
        step_periods=step_periods,
        max_folds=max_folds,
        anchored_enabled=anchored_enabled,
        rolling_enabled=rolling_enabled,
        holdout_enabled=False,
        uses_future_data=False,
        same_window_reuse_allowed=False,
        research_data_only=True,
        offline_backtest_research_only=True,
        window_kinds=[]
    )

    if anchored_enabled:
        policy.window_kinds.append(WalkForwardWindowKind.ANCHORED_EXPANDING)
    if rolling_enabled:
        policy.window_kinds.append(WalkForwardWindowKind.ROLLING_FIXED)

    errors = validate_walk_forward_window_policy(policy)
    policy.errors = errors
    policy.policy_valid = len(errors) == 0
    if not policy.policy_valid:
        policy.risk_flags.append(WalkForwardRiskFlag.WINDOW_POLICY_INVALID)

    return policy

def validate_walk_forward_window_policy(policy: WalkForwardWindowPolicy) -> List[str]:
    errors = []
    if policy.min_train_periods <= 0:
        errors.append("min_train_periods must be > 0")
    if policy.oos_periods <= 0:
        errors.append("oos_periods must be > 0")
    if policy.step_periods <= 0:
        errors.append("step_periods must be > 0")
    if policy.max_folds <= 0:
        errors.append("max_folds must be > 0")
    if policy.uses_future_data:
        errors.append("uses_future_data is strictly forbidden")
    if not policy.anchored_enabled and not policy.rolling_enabled:
        errors.append("At least one split type (anchored or rolling) must be enabled")
    return errors

def walk_forward_window_policy_summary(policy: WalkForwardWindowPolicy) -> Dict[str, Any]:
    return {
        "valid": policy.policy_valid,
        "train": policy.min_train_periods,
        "oos": policy.oos_periods,
        "step": policy.step_periods,
        "max_folds": policy.max_folds,
        "anchored": policy.anchored_enabled,
        "rolling": policy.rolling_enabled
    }

def walk_forward_window_policy_to_text(policy: WalkForwardWindowPolicy, limit: int = 300) -> str:
    lines = [
        f"WalkForwardWindowPolicy:",
        f"  Valid: {policy.policy_valid}",
        f"  Train: {policy.min_train_periods}, OOS: {policy.oos_periods}, Step: {policy.step_periods}",
        f"  Errors: {len(policy.errors)}"
    ]
    return "\n".join(lines)[:limit]
