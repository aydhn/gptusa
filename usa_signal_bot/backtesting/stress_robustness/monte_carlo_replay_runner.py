import datetime
import hashlib

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    MonteCarloPath,
    MonteCarloReplayResult,
    create_monte_carlo_replay_result_id
)

def run_monte_carlo_replays(paths: list[MonteCarloPath], initial_equity: float = 100000.0) -> list[MonteCarloReplayResult]:
    results = []
    for path in paths:
        results.append(run_single_monte_carlo_replay(path, initial_equity))
    return results

def run_single_monte_carlo_replay(path: MonteCarloPath, initial_equity: float = 100000.0) -> MonteCarloReplayResult:
    current_eq = initial_equity
    peak_eq = initial_equity
    max_dd = 0.0
    total_cost_penalty = 0.0
    min_eq = initial_equity

    base_cost = 0.001

    for i in range(len(path.returns)):
        ret = path.returns[i]
        cm = path.cost_multipliers[i]
        sm = path.slippage_multipliers[i]
        lh = path.liquidity_haircuts[i]

        # apply liquidity
        if ret > 0:
            ret *= (1.0 - lh)

        # apply costs
        penalty = base_cost * cm * sm
        ret -= penalty
        total_cost_penalty += penalty

        current_eq *= (1.0 + ret)

        if current_eq > peak_eq:
            peak_eq = current_eq
        if current_eq < min_eq:
            min_eq = current_eq

        if peak_eq > 0:
            dd = (peak_eq - current_eq) / peak_eq
            if dd > max_dd:
                max_dd = dd

    total_ret = (current_eq - initial_equity) / initial_equity

    res = MonteCarloReplayResult(
        result_id=create_monte_carlo_replay_result_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        path_id=path.path_id,
        method_kind=path.method_kind,
        path_index=path.path_index,
        final_equity=current_eq,
        total_return=total_ret,
        max_drawdown=max_dd,
        total_cost=total_cost_penalty * initial_equity,
        min_equity=min_eq,
        replay_hash=None,
        deterministic=True,
        simulated_only=True,
        real_order_created=False,
        broker_execution_used=False,
        paper_state_mutated=False,
        strategy_activation_allowed=False,
        investment_advice=False,
        research_data_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )

    res.replay_hash = compute_monte_carlo_replay_hash(res)
    return res

def compute_monte_carlo_replay_hash(result: MonteCarloReplayResult) -> str:
    s = f"{result.path_id}:{result.total_return}:{result.max_drawdown}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
