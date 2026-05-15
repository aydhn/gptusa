from typing import Dict, Any, Optional, List
from usa_signal_bot.regime_costs.regime_cost_models import CostRegimeSnapshot
from usa_signal_bot.core.enums import CombinedCostRegime

def attach_regime_costs_to_walk_forward_result(result: Dict[str, Any], snapshots_by_window: Optional[Dict[str, List[CostRegimeSnapshot]]] = None) -> Dict[str, Any]:
    result["metadata"] = result.get("metadata", {})
    if snapshots_by_window:
        dist_by_win = {}
        for win, snaps in snapshots_by_window.items():
            counts = {}
            for s in snaps:
                c = s.combined_regime.value
                counts[c] = counts.get(c, 0) + 1
            dist_by_win[win] = counts
        result["metadata"]["regime_distribution_by_window"] = dist_by_win
    return result

def walk_forward_regime_cost_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    meta = result.get("metadata", {})
    return {
        "regime_distribution_by_window": meta.get("regime_distribution_by_window", {})
    }

def walk_forward_regime_shift_warnings(result: Dict[str, Any]) -> List[str]:
    w = []
    meta = result.get("metadata", {})
    dist = meta.get("regime_distribution_by_window", {})
    for win, counts in dist.items():
        if counts.get("HIGH_RISK", 0) > 0:
            w.append(f"Window {win} contains HIGH_RISK regime trades.")
    return w

def classify_walk_forward_regime_cost_stability(result: Dict[str, Any]) -> CombinedCostRegime:
    meta = result.get("metadata", {})
    dist = meta.get("regime_distribution_by_window", {})

    total_high_risk = sum(counts.get("HIGH_RISK", 0) for counts in dist.values())
    if total_high_risk > 0:
        return CombinedCostRegime.HIGH_RISK
    return CombinedCostRegime.NORMAL
