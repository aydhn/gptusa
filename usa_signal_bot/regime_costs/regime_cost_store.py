import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from usa_signal_bot.regime_costs.regime_cost_models import (
    CostRegimeSnapshot, RegimeCostMultiplier, RegimeCostCurveSelection,
    AdaptiveExecutionRealismDecision, RegimeAwareCostBreakdown, RegimeCostReview,
    cost_regime_snapshot_to_dict, regime_cost_multiplier_to_dict,
    regime_cost_curve_selection_to_dict, adaptive_execution_realism_decision_to_dict,
    regime_aware_cost_breakdown_to_dict, regime_cost_review_to_dict
)

def regime_cost_store_dir(data_root: Path) -> Path:
    p = data_root / "regime_costs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def regime_snapshots_dir(data_root: Path) -> Path:
    p = regime_cost_store_dir(data_root) / "snapshots"
    p.mkdir(parents=True, exist_ok=True)
    return p

def regime_multipliers_dir(data_root: Path) -> Path:
    p = regime_cost_store_dir(data_root) / "multipliers"
    p.mkdir(parents=True, exist_ok=True)
    return p

def regime_curve_selections_dir(data_root: Path) -> Path:
    p = regime_cost_store_dir(data_root) / "curve_selections"
    p.mkdir(parents=True, exist_ok=True)
    return p

def adaptive_decisions_dir(data_root: Path) -> Path:
    p = regime_cost_store_dir(data_root) / "adaptive_decisions"
    p.mkdir(parents=True, exist_ok=True)
    return p

def regime_cost_breakdowns_dir(data_root: Path) -> Path:
    p = regime_cost_store_dir(data_root) / "breakdowns"
    p.mkdir(parents=True, exist_ok=True)
    return p

def regime_cost_reviews_dir(data_root: Path) -> Path:
    p = regime_cost_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_cost_regime_snapshot_json(path: Path, item: CostRegimeSnapshot) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cost_regime_snapshot_to_dict(item), f, indent=2)
    return path

def write_cost_regime_snapshots_jsonl(path: Path, items: List[CostRegimeSnapshot]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(cost_regime_snapshot_to_dict(it)) + "\n")
    return path

def write_regime_cost_multiplier_json(path: Path, item: RegimeCostMultiplier) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(regime_cost_multiplier_to_dict(item), f, indent=2)
    return path

def write_regime_cost_curve_selection_json(path: Path, item: RegimeCostCurveSelection) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(regime_cost_curve_selection_to_dict(item), f, indent=2)
    return path

def write_adaptive_execution_decision_json(path: Path, item: AdaptiveExecutionRealismDecision) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(adaptive_execution_realism_decision_to_dict(item), f, indent=2)
    return path

def write_regime_aware_cost_breakdown_json(path: Path, item: RegimeAwareCostBreakdown) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(regime_aware_cost_breakdown_to_dict(item), f, indent=2)
    return path

def write_regime_cost_review_json(path: Path, item: RegimeCostReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(regime_cost_review_to_dict(item), f, indent=2)
    return path

def read_regime_cost_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_regime_cost_reviews(data_root: Path) -> List[Path]:
    d = regime_cost_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_regime_cost_review(data_root: Path) -> Optional[Path]:
    l = list_regime_cost_reviews(data_root)
    return l[-1] if l else None

def regime_cost_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "snapshots_dir": str(regime_snapshots_dir(data_root)),
        "multipliers_dir": str(regime_multipliers_dir(data_root)),
        "curve_selections_dir": str(regime_curve_selections_dir(data_root)),
        "adaptive_decisions_dir": str(adaptive_decisions_dir(data_root)),
        "breakdowns_dir": str(regime_cost_breakdowns_dir(data_root)),
        "reviews_count": len(list_regime_cost_reviews(data_root))
    }
