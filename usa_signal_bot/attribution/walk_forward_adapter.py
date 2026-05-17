"""Adapter for integrating attribution with walk-forward results."""

from typing import Any, Dict, List
from usa_signal_bot.attribution.attribution_models import AttributionReview
from usa_signal_bot.attribution.backtest_adapter import build_attribution_review_from_backtest_result

def build_attribution_by_walk_forward_window(result: Dict[str, Any]) -> Dict[str, AttributionReview]:
    windows = result.get("windows", [])
    reviews = {}
    for i, w in enumerate(windows):
        reviews[f"window_{i}"] = build_attribution_review_from_backtest_result(w)
    return reviews

def attach_attribution_to_walk_forward_result(result: Dict[str, Any], reviews_by_window: Dict[str, AttributionReview] = None) -> Dict[str, Any]:
    if not reviews_by_window:
        reviews_by_window = build_attribution_by_walk_forward_window(result)

    result["attribution_metadata"] = {
        "window_reviews": {k: v.review_id for k, v in reviews_by_window.items()}
    }

    # Attach warnings for negative OOS
    for k, v in reviews_by_window.items():
        if v.scorecard and v.scorecard.total_net_pnl_usd < 0:
            result.setdefault("warnings", []).append(f"OOS window {k} has negative contributor")

    return result

def walk_forward_attribution_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("attribution_metadata", {})

def walk_forward_attribution_warnings(result: Dict[str, Any]) -> List[str]:
    return result.get("warnings", [])
