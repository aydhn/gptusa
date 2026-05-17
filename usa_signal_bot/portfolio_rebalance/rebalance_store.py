import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, DriftMeasurement,
    RebalanceAction, RebalancePlan, RebalanceReview,
    current_portfolio_state_to_dict, target_portfolio_state_to_dict,
    drift_measurement_to_dict, rebalance_action_to_dict,
    rebalance_plan_to_dict, rebalance_review_to_dict
)

def rebalance_store_dir(data_root: Path) -> Path:
    p = data_root / "portfolio_rebalance"
    p.mkdir(parents=True, exist_ok=True)
    return p

def current_states_dir(data_root: Path) -> Path:
    p = rebalance_store_dir(data_root) / "current_states"
    p.mkdir(exist_ok=True)
    return p

def target_states_dir(data_root: Path) -> Path:
    p = rebalance_store_dir(data_root) / "target_states"
    p.mkdir(exist_ok=True)
    return p

def drift_measurements_dir(data_root: Path) -> Path:
    p = rebalance_store_dir(data_root) / "drift_measurements"
    p.mkdir(exist_ok=True)
    return p

def rebalance_actions_dir(data_root: Path) -> Path:
    p = rebalance_store_dir(data_root) / "actions"
    p.mkdir(exist_ok=True)
    return p

def rebalance_plans_dir(data_root: Path) -> Path:
    p = rebalance_store_dir(data_root) / "plans"
    p.mkdir(exist_ok=True)
    return p

def rebalance_reviews_dir(data_root: Path) -> Path:
    p = rebalance_store_dir(data_root) / "reviews"
    p.mkdir(exist_ok=True)
    return p

def write_current_portfolio_state_json(path: Path, item: CurrentPortfolioState) -> Path:
    with open(path, "w") as f:
        json.dump(current_portfolio_state_to_dict(item), f, indent=2)
    return path

def write_target_portfolio_state_json(path: Path, item: TargetPortfolioState) -> Path:
    with open(path, "w") as f:
        json.dump(target_portfolio_state_to_dict(item), f, indent=2)
    return path

def write_drift_measurements_jsonl(path: Path, items: List[DriftMeasurement]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(drift_measurement_to_dict(item)) + "\n")
    return path

def write_rebalance_actions_jsonl(path: Path, items: List[RebalanceAction]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(rebalance_action_to_dict(item)) + "\n")
    return path

def write_rebalance_plan_json(path: Path, item: RebalancePlan) -> Path:
    with open(path, "w") as f:
        json.dump(rebalance_plan_to_dict(item), f, indent=2)
    return path

def write_rebalance_review_json(path: Path, item: RebalanceReview) -> Path:
    with open(path, "w") as f:
        json.dump(rebalance_review_to_dict(item), f, indent=2)
    return path

def read_rebalance_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_rebalance_reviews(data_root: Path) -> List[Path]:
    p = rebalance_reviews_dir(data_root)
    return sorted(list(p.glob("*.json")))

def get_latest_rebalance_review(data_root: Path) -> Optional[Path]:
    reviews = list_rebalance_reviews(data_root)
    if not reviews:
        return None
    return reviews[-1]

def rebalance_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "current_states": len(list(current_states_dir(data_root).glob("*.json"))),
        "target_states": len(list(target_states_dir(data_root).glob("*.json"))),
        "plans": len(list(rebalance_plans_dir(data_root).glob("*.json"))),
        "reviews": len(list_rebalance_reviews(data_root))
    }
