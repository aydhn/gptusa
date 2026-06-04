import datetime
import hashlib
import json
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    ScenarioPathPoint,
    ScenarioReplayResult,
    create_scenario_replay_result_id
)
from usa_signal_bot.core.enums import ScenarioReplayStatus

def run_scenario_replays(scenarios: list[StressScenario], paths: dict[str, list[ScenarioPathPoint]], initial_equity: float = 100000.0) -> list[ScenarioReplayResult]:
    results = []
    for scenario in scenarios:
        if scenario.scenario_id in paths:
            results.append(run_single_scenario_replay(scenario, paths[scenario.scenario_id], initial_equity))
    return results

def run_single_scenario_replay(scenario: StressScenario, points: list[ScenarioPathPoint], initial_equity: float = 100000.0) -> ScenarioReplayResult:
    current_equity = initial_equity
    peak_equity = initial_equity
    max_dd = 0.0

    total_cost_penalty = 0.0
    base_cost = 0.001 # approx 10 bps

    cost_mult = scenario.cost_multiplier if scenario.cost_multiplier else 1.0
    slip_mult = scenario.slippage_multiplier if scenario.slippage_multiplier else 1.0

    for p in points:
        ret = p.stressed_return if p.stressed_return is not None else 0.0

        # Apply cost/slippage penalty
        penalty = base_cost * cost_mult * slip_mult
        ret -= penalty
        total_cost_penalty += penalty

        current_equity *= (1.0 + ret)
        p.stressed_equity = current_equity

        if current_equity > peak_equity:
            peak_equity = current_equity

        if peak_equity > 0:
            dd = (peak_equity - current_equity) / peak_equity
            if dd > max_dd:
                max_dd = dd

        # Drawdown shock floor
        if scenario.drawdown_shock_floor is not None:
            if max_dd < scenario.drawdown_shock_floor:
                # Force drawdown if it hasn't reached floor by end of shock
                force_penalty = scenario.drawdown_shock_floor - max_dd
                if force_penalty > 0:
                    current_equity *= (1.0 - force_penalty)
                    max_dd = scenario.drawdown_shock_floor
                    p.stressed_equity = current_equity

    total_ret = (current_equity - initial_equity) / initial_equity

    res = ScenarioReplayResult(
        result_id=create_scenario_replay_result_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        scenario_id=scenario.scenario_id,
        scenario_kind=scenario.scenario_kind,
        severity_level=scenario.severity_level,
        replay_status=ScenarioReplayStatus.COMPLETED,
        path_points=points,
        final_stressed_equity=current_equity,
        stressed_total_return=total_ret,
        stressed_max_drawdown=max_dd,
        stressed_total_cost=total_cost_penalty * initial_equity, # approx
        replay_hash=None,
        deterministic=True,
        simulated_only=True,
        real_order_created=False,
        broker_execution_used=False,
        paper_state_mutated=False,
        strategy_activation_allowed=False,
        investment_advice=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"initial_equity": initial_equity}
    )

    res.replay_hash = compute_scenario_replay_hash(res)
    return res

def compute_scenario_replay_hash(result: ScenarioReplayResult) -> str:
    s = f"{result.scenario_id}:{result.stressed_total_return}:{result.stressed_max_drawdown}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
