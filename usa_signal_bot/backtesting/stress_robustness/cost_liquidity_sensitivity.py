import datetime
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    ScenarioReplayResult,
    CostLiquiditySensitivityResult,
    create_cost_liquidity_sensitivity_id
)
from usa_signal_bot.core.enums import StressScenarioKind

def build_cost_liquidity_sensitivity(scenarios: list[StressScenario], results: list[ScenarioReplayResult]) -> CostLiquiditySensitivityResult:
    cost_score = calculate_cost_sensitivity_score(scenarios, results)
    slip_score = calculate_slippage_sensitivity_score(scenarios, results)
    liq_score = calculate_liquidity_sensitivity_score(scenarios, results)

    scores = [s for s in [cost_score, slip_score, liq_score] if s is not None]
    comb = sum(scores) / len(scores) if scores else None

    return CostLiquiditySensitivityResult(
        sensitivity_id=create_cost_liquidity_sensitivity_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        scenario_count=len(scenarios),
        cost_sensitivity_score=cost_score,
        slippage_sensitivity_score=slip_score,
        liquidity_sensitivity_score=liq_score,
        combined_sensitivity_score=comb,
        sensitivity_notes=["Sensitivity computed via deterministic path degradation."],
        sensitivity_valid=True,
        not_strategy_activation=True,
        not_investment_advice=True,
        research_data_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )

def calculate_cost_sensitivity_score(scenarios: list[StressScenario], results: list[ScenarioReplayResult]) -> float | None:
    return _calc_sensitivity(scenarios, results, StressScenarioKind.COST_SHOCK)

def calculate_slippage_sensitivity_score(scenarios: list[StressScenario], results: list[ScenarioReplayResult]) -> float | None:
    return _calc_sensitivity(scenarios, results, StressScenarioKind.SLIPPAGE_SHOCK)

def calculate_liquidity_sensitivity_score(scenarios: list[StressScenario], results: list[ScenarioReplayResult]) -> float | None:
    return _calc_sensitivity(scenarios, results, StressScenarioKind.LIQUIDITY_SHOCK)

def _calc_sensitivity(scenarios: list[StressScenario], results: list[ScenarioReplayResult], kind: StressScenarioKind) -> float | None:
    target_ids = [s.scenario_id for s in scenarios if s.scenario_kind == kind]
    if not target_ids:
        return None

    target_results = [r for r in results if r.scenario_id in target_ids]
    if not target_results:
        return None

    avg_dd = sum(r.stressed_max_drawdown for r in target_results if r.stressed_max_drawdown) / len(target_results)
    return avg_dd
