
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, CostStressedBacktestResult, ExecutionSensitivityMatrix,
    WalkForwardCostRobustnessResult, CostFragilityAssessment, CostRobustnessReview,
    cost_stress_scenario_to_dict, cost_stressed_backtest_result_to_dict,
    execution_sensitivity_matrix_to_dict, walk_forward_cost_robustness_result_to_dict,
    cost_fragility_assessment_to_dict, cost_robustness_review_to_dict
)

def robustness_store_dir(data_root: Path) -> Path:
    d = data_root / "cost_robustness"
    d.mkdir(parents=True, exist_ok=True)
    return d

def stress_scenarios_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "scenarios"
    d.mkdir(parents=True, exist_ok=True)
    return d

def stressed_results_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "stressed_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sensitivity_matrices_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "sensitivity_matrices"
    d.mkdir(parents=True, exist_ok=True)
    return d

def walk_forward_cost_robustness_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "walk_forward"
    d.mkdir(parents=True, exist_ok=True)
    return d

def fragility_assessments_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "fragility"
    d.mkdir(parents=True, exist_ok=True)
    return d

def robustness_reviews_dir(data_root: Path) -> Path:
    d = robustness_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_cost_stress_scenarios_json(path: Path, scenarios: List[CostStressScenario]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump([cost_stress_scenario_to_dict(s) for s in scenarios], f, indent=2)
    return path

def write_cost_stressed_backtest_result_json(path: Path, result: CostStressedBacktestResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(cost_stressed_backtest_result_to_dict(result), f, indent=2)
    return path

def write_execution_sensitivity_matrix_json(path: Path, matrix: ExecutionSensitivityMatrix) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(execution_sensitivity_matrix_to_dict(matrix), f, indent=2)
    return path

def write_walk_forward_cost_robustness_result_json(path: Path, result: WalkForwardCostRobustnessResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(walk_forward_cost_robustness_result_to_dict(result), f, indent=2)
    return path

def write_cost_fragility_assessment_json(path: Path, assessment: CostFragilityAssessment) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(cost_fragility_assessment_to_dict(assessment), f, indent=2)
    return path

def write_cost_robustness_review_json(path: Path, review: CostRobustnessReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(cost_robustness_review_to_dict(review), f, indent=2)
    return path

def read_cost_robustness_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def list_cost_robustness_reviews(data_root: Path) -> List[Path]:
    d = robustness_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_cost_robustness_review(data_root: Path) -> Optional[Path]:
    files = list_cost_robustness_reviews(data_root)
    return files[-1] if files else None

def robustness_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews_count": len(list_cost_robustness_reviews(data_root))
    }
