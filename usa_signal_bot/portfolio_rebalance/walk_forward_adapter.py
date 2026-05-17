from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceReview

def attach_rebalance_to_walk_forward_result(result: Dict[str, Any], reviews_by_window: Optional[Dict[str, RebalanceReview]] = None) -> Dict[str, Any]:
    if reviews_by_window:
        from usa_signal_bot.portfolio_rebalance.rebalance_models import rebalance_review_to_dict
        result["rebalance_metadata_by_window"] = {k: rebalance_review_to_dict(v) for k, v in reviews_by_window.items()}
    return result

def walk_forward_rebalance_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    if "rebalance_metadata_by_window" not in result:
        return {}
    meta = result["rebalance_metadata_by_window"]
    high_turnover_windows = sum(1 for v in meta.values() if v.get("plan", {}).get("turnover_assessment", {}).get("status") in ["HIGH", "EXCESSIVE"])
    return {
        "windows_with_rebalance_metadata": len(meta),
        "high_turnover_windows": high_turnover_windows
    }

def walk_forward_turnover_stability(result: Dict[str, Any]) -> Dict[str, Any]:
    if "rebalance_metadata_by_window" not in result:
        return {"stability": "UNKNOWN"}

    meta = result["rebalance_metadata_by_window"]
    excessive_count = sum(1 for v in meta.values() if v.get("plan", {}).get("turnover_assessment", {}).get("status") == "EXCESSIVE")

    stability = "STABLE"
    if excessive_count > 0:
        stability = "UNSTABLE"

    return {
        "stability": stability,
        "excessive_turnover_windows": excessive_count
    }

def walk_forward_rebalance_warnings(result: Dict[str, Any]) -> List[str]:
    warnings = []
    stability = walk_forward_turnover_stability(result)
    if stability.get("stability") == "UNSTABLE":
        warnings.append(f"Walk-forward unstable due to {stability.get('excessive_turnover_windows')} windows with EXCESSIVE turnover.")
    return warnings
