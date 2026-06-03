from typing import Any, Dict, List

from usa_signal_bot.core.enums import WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardFold,
    FoldReplayConfig,
    create_fold_replay_config_id,
    _now_utc
)

def build_fold_replay_configs(folds: List[WalkForwardFold], initial_cash: float = 100000.0, deterministic_seed: int = 150) -> List[FoldReplayConfig]:
    configs = []
    for f in folds:
        config = FoldReplayConfig(
            config_id=create_fold_replay_config_id(),
            created_at_utc=_now_utc(),
            fold_id=f.fold_id,
            fold_index=f.fold_index,
            deterministic_seed=deterministic_seed,
            initial_cash=initial_cash,
            cost_model_ref=None,
            benchmark_ref=None,
            replay_valid=True,
            offline_replay_only=True,
            live_trading_enabled=False,
            paper_trading_enabled=False,
            broker_execution_enabled=False,
            real_order_creation_enabled=False,
            paper_state_mutation_enabled=False,
            strategy_activation_allowed=False,
            portfolio_optimization_enabled=False
        )
        errors = validate_fold_replay_configs([config])
        if errors:
            config.replay_valid = False
            config.errors = errors
            config.risk_flags.append(WalkForwardRiskFlag.FOLD_REPLAY_CONFIG_INVALID)
        configs.append(config)
    return configs

def validate_fold_replay_configs(items: List[FoldReplayConfig]) -> List[str]:
    errors = []
    for c in items:
        if not c.offline_replay_only:
            errors.append(f"Config {c.config_id} offline_replay_only must be true")
        if c.live_trading_enabled:
            errors.append(f"Config {c.config_id} live_trading_enabled must be false")
        if c.paper_trading_enabled:
            errors.append(f"Config {c.config_id} paper_trading_enabled must be false")
        if c.broker_execution_enabled:
            errors.append(f"Config {c.config_id} broker_execution_enabled must be false")
        if c.real_order_creation_enabled:
            errors.append(f"Config {c.config_id} real_order_creation_enabled must be false")
        if c.paper_state_mutation_enabled:
            errors.append(f"Config {c.config_id} paper_state_mutation_enabled must be false")
        if c.strategy_activation_allowed:
            errors.append(f"Config {c.config_id} strategy_activation_allowed must be false")
        if c.portfolio_optimization_enabled:
            errors.append(f"Config {c.config_id} portfolio_optimization_enabled must be false")
    return errors

def fold_replay_configs_summary(items: List[FoldReplayConfig]) -> Dict[str, Any]:
    valid_count = sum(1 for c in items if c.replay_valid)
    return {
        "total_configs": len(items),
        "valid_configs": valid_count,
        "all_valid": valid_count == len(items) and len(items) > 0
    }

def fold_replay_configs_to_text(items: List[FoldReplayConfig], limit: int = 300) -> str:
    summary = fold_replay_configs_summary(items)
    return f"Fold Replay Configs: {summary['valid_configs']}/{summary['total_configs']} valid"
