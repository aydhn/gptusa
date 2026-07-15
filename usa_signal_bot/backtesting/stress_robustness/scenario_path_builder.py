import datetime
import pandas as pd
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    ScenarioPathPoint,
    create_scenario_path_point_id
)
from usa_signal_bot.core.enums import StressScenarioKind

def build_scenario_paths(scenarios: list[StressScenario], return_df: pd.DataFrame, equity_df: pd.DataFrame | None = None) -> dict[str, list[ScenarioPathPoint]]:
    paths = {}
    for scenario in scenarios:
        paths[scenario.scenario_id] = build_path_for_scenario(scenario, return_df, equity_df)
    return paths

def build_path_for_scenario(scenario: StressScenario, return_df: pd.DataFrame, equity_df: pd.DataFrame | None = None) -> list[ScenarioPathPoint]:
    points = []

    ret_col = "return"
    if ret_col not in return_df.columns:
        if "returns" in return_df.columns:
            ret_col = "returns"
        elif "strategy_return" in return_df.columns:
            ret_col = "strategy_return"

    has_equity = equity_df is not None and ("equity" in equity_df.columns or "balance" in equity_df.columns)
    eq_col = "equity" if has_equity and "equity" in equity_df.columns else "balance"

    total_count = len(return_df)

    idx_arr = return_df.index
    ret_arr = return_df[ret_col].values
    eq_arr = equity_df[eq_col].values if has_equity else None

    for i in range(total_count):
        orig_ret = ret_arr[i]
        stressed_ret = apply_stress_to_return(orig_ret, scenario, i, total_count)

        orig_eq = eq_arr[i] if has_equity else None

        points.append(ScenarioPathPoint(
            point_id=create_scenario_path_point_id(),
            created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
            scenario_id=scenario.scenario_id,
            timestamp=str(idx_arr[i]),
            original_return=orig_ret,
            stressed_return=stressed_ret,
            original_equity=orig_eq,
            stressed_equity=None, # Will be computed in replay
            cost_multiplier_applied=scenario.cost_multiplier,
            liquidity_haircut_applied=scenario.liquidity_haircut,
            point_valid=True,
            research_data_only=True,
            investment_advice=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"index": i}
        ))

    return points

def apply_stress_to_return(original_return: float | None, scenario: StressScenario, index: int, total_count: int) -> float | None:
    if original_return is None:
        return None

    stressed = original_return

    # Gap risk
    if scenario.gap_return_shock is not None and index == total_count // 2:
        stressed += scenario.gap_return_shock

    # Missing data
    if scenario.missing_data_fraction is not None:
        if (index * 7) % 100 < (scenario.missing_data_fraction * 100):
            return 0.0 # Missing return maps to 0 for path

    if scenario.return_shock_multiplier is not None:
        if stressed > 0:
            stressed *= scenario.return_shock_multiplier
        else:
            stressed *= (1 + (1 - scenario.return_shock_multiplier)) # magnify losses

    if scenario.volatility_multiplier is not None:
        stressed *= scenario.volatility_multiplier

    if scenario.liquidity_haircut is not None and stressed > 0:
        stressed *= (1.0 - scenario.liquidity_haircut)

    return stressed
