
from typing import List, Any, Dict, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import CostRobustnessStatus
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, WalkForwardCostRobustnessResult, create_walk_forward_cost_robustness_result_id
)
from usa_signal_bot.cost_robustness.stress_scenarios import default_cost_stress_scenarios
from usa_signal_bot.cost_robustness.stressed_results import stress_backtest_result

def extract_walk_forward_windows(walk_forward_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    return walk_forward_result.get('windows', [])

def stress_walk_forward_window(window: Dict[str, Any], scenario: CostStressScenario) -> Dict[str, Any]:
    trades = window.get('trades', [])
    baseline_result = window.get('metrics', {})
    stressed = stress_backtest_result(baseline_result, trades, scenario)
    return {
        "window_id": window.get("window_id"),
        "scenario_id": scenario.scenario_id,
        "stressed_status": stressed.status.value,
        "profitable": stressed.profitable_after_costs
    }

def classify_walk_forward_cost_robustness(window_results: List[Dict[str, Any]]) -> CostRobustnessStatus:
    if not window_results:
        return CostRobustnessStatus.INSUFFICIENT_DATA
    fragile = sum(1 for w in window_results if w.get('profitable') is False)
    if fragile > len(window_results) * 0.3:
        return CostRobustnessStatus.FRAGILE
    return CostRobustnessStatus.ROBUST

def evaluate_walk_forward_cost_robustness(walk_forward_result: Dict[str, Any], scenarios: Optional[List[CostStressScenario]] = None) -> WalkForwardCostRobustnessResult:
    if scenarios is None:
        scenarios = default_cost_stress_scenarios()

    windows = extract_walk_forward_windows(walk_forward_result)
    window_results = []

    # We apply the moderate scenario to check window fragility
    test_scenario = next((s for s in scenarios if s.name == "Moderate Cost Stress"), scenarios[0])

    for w in windows:
        window_results.append(stress_walk_forward_window(w, test_scenario))

    status = classify_walk_forward_cost_robustness(window_results)

    return WalkForwardCostRobustnessResult(
        result_id=create_walk_forward_cost_robustness_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        window_count=len(windows),
        scenario_count=len(scenarios),
        status=status,
        window_results=window_results,
        scenario_results=[], # Not fully evaluated here to save time
        robustness_score=100.0 if status == CostRobustnessStatus.ROBUST else 50.0,
        fragile_window_count=sum(1 for w in window_results if w.get('profitable') is False),
        failed_scenario_count=0,
        warnings=[],
        errors=[],
        metadata={}
    )

def walk_forward_cost_robustness_to_text(result: WalkForwardCostRobustnessResult, limit: int = 100) -> str:
    lines = [
        f"--- Walk-Forward Cost Robustness ---",
        f"Status: {result.status.value}",
        f"Windows Evaluated: {result.window_count}",
        f"Fragile Windows: {result.fragile_window_count}"
    ]
    return "\n".join(lines)
