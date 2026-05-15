from typing import Dict, Any, Optional, List
from usa_signal_bot.regime_costs.regime_cost_models import CostRegimeSnapshot

def attach_regime_costs_to_basket_result(result: Dict[str, Any], snapshots: Optional[List[CostRegimeSnapshot]] = None) -> Dict[str, Any]:
    result["metadata"] = result.get("metadata", {})
    if snapshots:
        counts = {}
        for s in snapshots:
            c = s.combined_regime.value
            counts[c] = counts.get(c, 0) + 1
        result["metadata"]["basket_regime_concentration"] = counts
    return result

def basket_regime_cost_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    meta = result.get("metadata", {})
    return {
        "basket_regime_concentration": meta.get("basket_regime_concentration", {})
    }

def basket_regime_concentration_warnings(result: Dict[str, Any]) -> List[str]:
    w = []
    meta = result.get("metadata", {})
    conc = meta.get("basket_regime_concentration", {})

    if conc.get("HIGH_RISK", 0) > 0 or conc.get("BLOCKED", 0) > 0:
        w.append("Basket contains symbols in HIGH_RISK or BLOCKED regimes.")
    return w
