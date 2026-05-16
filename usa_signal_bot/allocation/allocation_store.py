import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.exceptions import AllocationStorageError
from usa_signal_bot.allocation.allocation_models import (
    CapitalState, RiskBudget, PositionSizeResult, AllocationReview,
    capital_state_to_dict, risk_budget_to_dict, position_size_result_to_dict, allocation_review_to_dict
)

def allocation_store_dir(data_root: Path) -> Path:
    return data_root / "allocation"

def capital_states_dir(data_root: Path) -> Path:
    return allocation_store_dir(data_root) / "capital_states"

def risk_budgets_dir(data_root: Path) -> Path:
    return allocation_store_dir(data_root) / "risk_budgets"

def sizing_results_dir(data_root: Path) -> Path:
    return allocation_store_dir(data_root) / "sizing_results"

def allocation_reviews_dir(data_root: Path) -> Path:
    return allocation_store_dir(data_root) / "reviews"

def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_capital_state_json(path: Path, item: CapitalState) -> Path:
    _ensure_dir(path.parent)
    try:
        with open(path, "w") as f:
            json.dump(capital_state_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise AllocationStorageError(f"Failed to write capital state: {e}")

def write_risk_budget_json(path: Path, item: RiskBudget) -> Path:
    _ensure_dir(path.parent)
    try:
        with open(path, "w") as f:
            json.dump(risk_budget_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise AllocationStorageError(f"Failed to write risk budget: {e}")

def write_position_size_result_json(path: Path, item: PositionSizeResult) -> Path:
    _ensure_dir(path.parent)
    try:
        with open(path, "w") as f:
            json.dump(position_size_result_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise AllocationStorageError(f"Failed to write position size result: {e}")

def write_position_size_results_jsonl(path: Path, items: List[PositionSizeResult]) -> Path:
    _ensure_dir(path.parent)
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(position_size_result_to_dict(item)) + "\n")
        return path
    except Exception as e:
        raise AllocationStorageError(f"Failed to write position size results JSONL: {e}")

def write_allocation_review_json(path: Path, item: AllocationReview) -> Path:
    _ensure_dir(path.parent)
    try:
        with open(path, "w") as f:
            json.dump(allocation_review_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise AllocationStorageError(f"Failed to write allocation review: {e}")

def read_allocation_review_json(path: Path) -> Dict[str, Any]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise AllocationStorageError(f"Failed to read allocation review: {e}")

def list_allocation_reviews(data_root: Path) -> List[Path]:
    d = allocation_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_allocation_review(data_root: Path) -> Optional[Path]:
    files = list_allocation_reviews(data_root)
    if files:
        return files[0]
    return None

def allocation_store_summary(data_root: Path) -> Dict[str, Any]:
    d = allocation_store_dir(data_root)
    if not d.exists():
        return {"exists": False}

    return {
        "exists": True,
        "capital_states_count": len(list(capital_states_dir(data_root).glob("*.json"))) if capital_states_dir(data_root).exists() else 0,
        "risk_budgets_count": len(list(risk_budgets_dir(data_root).glob("*.json"))) if risk_budgets_dir(data_root).exists() else 0,
        "reviews_count": len(list(allocation_reviews_dir(data_root).glob("*.json"))) if allocation_reviews_dir(data_root).exists() else 0,
    }
