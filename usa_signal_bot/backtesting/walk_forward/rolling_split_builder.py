from typing import Any, Dict, List

from usa_signal_bot.core.enums import WalkForwardFoldKind, WalkForwardFoldStatus, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardFold,
    WalkForwardWindowPolicy,
    create_walk_forward_fold_id,
    _now_utc
)

def build_rolling_walk_forward_folds(strategy_return_df: Any, policy: WalkForwardWindowPolicy) -> List[WalkForwardFold]:
    folds = []
    if not policy.rolling_enabled or not policy.policy_valid:
        return folds

    if strategy_return_df is None or len(strategy_return_df) == 0:
        return folds

    df = strategy_return_df
    total_len = len(df)
    train_start_idx = 0
    current_train_end = policy.min_train_periods
    fold_idx = 1

    while current_train_end + policy.oos_periods <= total_len and fold_idx <= policy.max_folds:
        oos_start_idx = current_train_end
        oos_end_idx = current_train_end + policy.oos_periods

        train_start = str(df.iloc[train_start_idx]['timestamp']) if 'timestamp' in df.columns else str(train_start_idx)
        train_end = str(df.iloc[current_train_end - 1]['timestamp']) if 'timestamp' in df.columns else str(current_train_end - 1)
        oos_start = str(df.iloc[oos_start_idx]['timestamp']) if 'timestamp' in df.columns else str(oos_start_idx)
        oos_end = str(df.iloc[oos_end_idx - 1]['timestamp']) if 'timestamp' in df.columns else str(oos_end_idx - 1)

        fold = WalkForwardFold(
            fold_id=create_walk_forward_fold_id(),
            created_at_utc=_now_utc(),
            fold_kind=WalkForwardFoldKind.ROLLING_FOLD,
            fold_index=fold_idx,
            train_start=train_start,
            train_end=train_end,
            oos_start=oos_start,
            oos_end=oos_end,
            train_row_count=current_train_end - train_start_idx,
            oos_row_count=policy.oos_periods,
            fold_status=WalkForwardFoldStatus.CREATED,
            no_lookahead=True,
            research_data_only=True
        )
        errors = validate_rolling_folds([fold])
        if errors:
            fold.fold_status = WalkForwardFoldStatus.INVALID
            fold.errors = errors
            fold.risk_flags.append(WalkForwardRiskFlag.ROLLING_SPLIT_INVALID)
        else:
            fold.fold_status = WalkForwardFoldStatus.VALID

        folds.append(fold)

        train_start_idx += policy.step_periods
        current_train_end += policy.step_periods
        fold_idx += 1

    return folds

def validate_rolling_folds(folds: List[WalkForwardFold]) -> List[str]:
    errors = []
    for f in folds:
        if f.fold_kind != WalkForwardFoldKind.ROLLING_FOLD:
            errors.append(f"Fold {f.fold_index} is not ROLLING_FOLD")
        if not f.no_lookahead:
            errors.append(f"Fold {f.fold_index} lookahead detected")
        if f.train_row_count <= 0 or f.oos_row_count <= 0:
            errors.append(f"Fold {f.fold_index} has empty windows")
    return errors

def rolling_folds_summary(folds: List[WalkForwardFold]) -> Dict[str, Any]:
    valid_count = sum(1 for f in folds if f.fold_status == WalkForwardFoldStatus.VALID)
    return {
        "total_folds": len(folds),
        "valid_folds": valid_count,
        "all_valid": valid_count == len(folds) and len(folds) > 0
    }

def rolling_folds_to_text(folds: List[WalkForwardFold], limit: int = 300) -> str:
    summary = rolling_folds_summary(folds)
    return f"Rolling Splits: {summary['valid_folds']}/{summary['total_folds']} valid"
