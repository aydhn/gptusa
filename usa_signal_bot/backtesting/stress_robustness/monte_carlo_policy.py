import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    MonteCarloPolicy,
    create_monte_carlo_policy_id
)
from usa_signal_bot.core.enums import MonteCarloMethodKind

def build_default_monte_carlo_policy() -> MonteCarloPolicy:
    return build_custom_monte_carlo_policy(path_count=250, deterministic_seed=151, block_size=20)

def build_custom_monte_carlo_policy(path_count: int, deterministic_seed: int = 151, block_size: int | None = 20) -> MonteCarloPolicy:
    valid = path_count > 0
    errors = []
    if not valid:
        errors.append("path_count must be > 0")

    return MonteCarloPolicy(
        policy_id=create_monte_carlo_policy_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        method_kinds=[
            MonteCarloMethodKind.RETURN_BOOTSTRAP,
            MonteCarloMethodKind.BLOCK_BOOTSTRAP,
            MonteCarloMethodKind.RETURN_PERMUTATION,
            MonteCarloMethodKind.PATH_PERTURBATION,
            MonteCarloMethodKind.COST_SLIPPAGE_PERTURBATION
        ],
        deterministic_seed=deterministic_seed,
        path_count=path_count,
        block_size=block_size,
        perturb_costs=True,
        perturb_slippage=True,
        perturb_liquidity=True,
        max_return_perturbation_abs=0.02,
        max_cost_multiplier=3.0,
        max_slippage_multiplier=3.0,
        policy_valid=valid,
        deterministic=True,
        research_data_only=True,
        offline_backtest_research_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
