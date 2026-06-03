import datetime
import hashlib
import random
import pandas as pd

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    MonteCarloPolicy,
    MonteCarloPath,
    create_monte_carlo_path_id
)
from usa_signal_bot.core.enums import MonteCarloMethodKind, MonteCarloPathStatus

def build_monte_carlo_paths(return_df: pd.DataFrame, policy: MonteCarloPolicy) -> list[MonteCarloPath]:
    paths = []
    ret_col = "return"
    if ret_col not in return_df.columns:
        if "returns" in return_df.columns:
            ret_col = "returns"
        elif "strategy_return" in return_df.columns:
            ret_col = "strategy_return"

    base_returns = return_df[ret_col].fillna(0.0).tolist()

    # Her method için path_count / method_count kadar path üretelim
    methods = policy.method_kinds
    paths_per_method = max(1, policy.path_count // len(methods))

    idx = 0
    for method in methods:
        for _ in range(paths_per_method):
            if method == MonteCarloMethodKind.RETURN_BOOTSTRAP:
                p = build_return_bootstrap_path(base_returns, idx, policy)
            elif method == MonteCarloMethodKind.BLOCK_BOOTSTRAP:
                p = build_block_bootstrap_path(base_returns, idx, policy)
            elif method == MonteCarloMethodKind.RETURN_PERMUTATION:
                p = build_permutation_path(base_returns, idx, policy)
            elif method == MonteCarloMethodKind.PATH_PERTURBATION:
                p = build_path_perturbation_path(base_returns, idx, policy)
            else: # COST_SLIPPAGE_PERTURBATION
                p = build_cost_slippage_path(base_returns, idx, policy)
            paths.append(p)
            idx += 1
            if idx >= policy.path_count:
                break
        if idx >= policy.path_count:
            break

    return paths

def _create_base_path(returns: list[float], method: MonteCarloMethodKind, index: int, policy: MonteCarloPolicy) -> MonteCarloPath:
    p = MonteCarloPath(
        path_id=create_monte_carlo_path_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        method_kind=method,
        path_index=index,
        deterministic_seed=policy.deterministic_seed + index,
        path_status=MonteCarloPathStatus.CREATED,
        returns=returns,
        cost_multipliers=[1.0] * len(returns),
        slippage_multipliers=[1.0] * len(returns),
        liquidity_haircuts=[0.0] * len(returns),
        path_hash=None,
        deterministic=True,
        research_data_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    return p

def build_return_bootstrap_path(returns: list[float], index: int, policy: MonteCarloPolicy) -> MonteCarloPath:
    rng = random.Random(policy.deterministic_seed + index)
    new_rets = [rng.choice(returns) for _ in returns]
    p = _create_base_path(new_rets, MonteCarloMethodKind.RETURN_BOOTSTRAP, index, policy)
    p.path_hash = compute_monte_carlo_path_hash(p)
    return p

def build_block_bootstrap_path(returns: list[float], index: int, policy: MonteCarloPolicy) -> MonteCarloPath:
    rng = random.Random(policy.deterministic_seed + index)
    bs = policy.block_size if policy.block_size else 20
    n = len(returns)
    new_rets = []
    while len(new_rets) < n:
        start = rng.randint(0, max(0, n - bs))
        new_rets.extend(returns[start:start+bs])
    new_rets = new_rets[:n]
    p = _create_base_path(new_rets, MonteCarloMethodKind.BLOCK_BOOTSTRAP, index, policy)
    p.path_hash = compute_monte_carlo_path_hash(p)
    return p

def build_permutation_path(returns: list[float], index: int, policy: MonteCarloPolicy) -> MonteCarloPath:
    rng = random.Random(policy.deterministic_seed + index)
    new_rets = list(returns)
    rng.shuffle(new_rets)
    p = _create_base_path(new_rets, MonteCarloMethodKind.RETURN_PERMUTATION, index, policy)
    p.path_hash = compute_monte_carlo_path_hash(p)
    return p

def build_path_perturbation_path(returns: list[float], index: int, policy: MonteCarloPolicy) -> MonteCarloPath:
    rng = random.Random(policy.deterministic_seed + index)
    max_p = policy.max_return_perturbation_abs if policy.max_return_perturbation_abs else 0.02
    new_rets = []
    for r in returns:
        noise = rng.uniform(-max_p, max_p)
        new_rets.append(r + noise)
    p = _create_base_path(new_rets, MonteCarloMethodKind.PATH_PERTURBATION, index, policy)
    p.path_hash = compute_monte_carlo_path_hash(p)
    return p

def build_cost_slippage_path(returns: list[float], index: int, policy: MonteCarloPolicy) -> MonteCarloPath:
    rng = random.Random(policy.deterministic_seed + index)
    max_c = policy.max_cost_multiplier if policy.max_cost_multiplier else 3.0
    max_s = policy.max_slippage_multiplier if policy.max_slippage_multiplier else 3.0

    p = _create_base_path(list(returns), MonteCarloMethodKind.COST_SLIPPAGE_PERTURBATION, index, policy)
    if policy.perturb_costs:
        p.cost_multipliers = [rng.uniform(1.0, max_c) for _ in returns]
    if policy.perturb_slippage:
        p.slippage_multipliers = [rng.uniform(1.0, max_s) for _ in returns]
    if policy.perturb_liquidity:
        p.liquidity_haircuts = [rng.uniform(0.0, 0.5) for _ in returns]

    p.path_hash = compute_monte_carlo_path_hash(p)
    return p

def compute_monte_carlo_path_hash(path: MonteCarloPath) -> str:
    s = f"{path.method_kind}:{path.path_index}:{sum(path.returns):.4f}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
