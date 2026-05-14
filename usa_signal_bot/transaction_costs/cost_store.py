import json
from pathlib import Path
from typing import Any

from usa_signal_bot.transaction_costs.cost_models import (
    TransactionCostBreakdown,
    SlippageCurve,
    MarketImpactEstimate,
    FillSimulationResult,
    CostAdjustedTradeResult,
    TransactionCostReview,
    transaction_cost_breakdown_to_dict,
    slippage_curve_to_dict,
    market_impact_estimate_to_dict,
    fill_simulation_result_to_dict,
    cost_adjusted_trade_result_to_dict,
    transaction_cost_review_to_dict
)

def cost_store_dir(data_root: Path) -> Path:
    d = data_root / "transaction_costs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def cost_breakdowns_dir(data_root: Path) -> Path:
    d = cost_store_dir(data_root) / "breakdowns"
    d.mkdir(parents=True, exist_ok=True)
    return d

def slippage_curves_dir(data_root: Path) -> Path:
    d = cost_store_dir(data_root) / "slippage_curves"
    d.mkdir(parents=True, exist_ok=True)
    return d

def market_impact_dir(data_root: Path) -> Path:
    d = cost_store_dir(data_root) / "market_impact"
    d.mkdir(parents=True, exist_ok=True)
    return d

def fill_simulations_dir(data_root: Path) -> Path:
    d = cost_store_dir(data_root) / "fill_simulations"
    d.mkdir(parents=True, exist_ok=True)
    return d

def cost_adjusted_trades_dir(data_root: Path) -> Path:
    d = cost_store_dir(data_root) / "adjusted_trades"
    d.mkdir(parents=True, exist_ok=True)
    return d

def cost_reviews_dir(data_root: Path) -> Path:
    d = cost_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path

def write_transaction_cost_breakdown_json(path: Path, item: TransactionCostBreakdown) -> Path:
    return _write_json(path, transaction_cost_breakdown_to_dict(item))

def write_slippage_curve_json(path: Path, item: SlippageCurve) -> Path:
    return _write_json(path, slippage_curve_to_dict(item))

def write_market_impact_estimate_json(path: Path, item: MarketImpactEstimate) -> Path:
    return _write_json(path, market_impact_estimate_to_dict(item))

def write_fill_simulation_result_json(path: Path, item: FillSimulationResult) -> Path:
    return _write_json(path, fill_simulation_result_to_dict(item))

def write_cost_adjusted_trade_result_json(path: Path, item: CostAdjustedTradeResult) -> Path:
    return _write_json(path, cost_adjusted_trade_result_to_dict(item))

def write_transaction_cost_review_json(path: Path, item: TransactionCostReview) -> Path:
    return _write_json(path, transaction_cost_review_to_dict(item))

def read_transaction_cost_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_transaction_cost_reviews(data_root: Path) -> list[Path]:
    d = cost_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_transaction_cost_review(data_root: Path) -> Path | None:
    reviews = list_transaction_cost_reviews(data_root)
    if not reviews:
        return None
    # Sort by name (which has timestamp)
    return sorted(reviews)[-1]

def cost_store_summary(data_root: Path) -> dict[str, Any]:
    b_count = len(list(cost_breakdowns_dir(data_root).glob("*.json")))
    c_count = len(list(slippage_curves_dir(data_root).glob("*.json")))
    m_count = len(list(market_impact_dir(data_root).glob("*.json")))
    f_count = len(list(fill_simulations_dir(data_root).glob("*.json")))
    a_count = len(list(cost_adjusted_trades_dir(data_root).glob("*.json")))
    r_count = len(list(cost_reviews_dir(data_root).glob("*.json")))

    return {
        "breakdowns": b_count,
        "slippage_curves": c_count,
        "market_impacts": m_count,
        "fill_simulations": f_count,
        "adjusted_trades": a_count,
        "reviews": r_count
    }
