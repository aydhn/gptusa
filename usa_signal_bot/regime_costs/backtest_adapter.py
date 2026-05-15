from typing import Dict, Any, Optional, List
from usa_signal_bot.regime_costs.regime_cost_models import CostRegimeSnapshot, RegimeAwareCostBreakdown

def attach_regime_costs_to_backtest_trade(trade: Dict[str, Any], snapshot: Optional[CostRegimeSnapshot] = None, regime_breakdown: Optional[RegimeAwareCostBreakdown] = None) -> Dict[str, Any]:
    trade["metadata"] = trade.get("metadata", {})
    if snapshot:
        trade["metadata"]["cost_regime"] = snapshot.combined_regime.value
    if regime_breakdown:
        trade["metadata"]["regime_cost_curve_profile"] = regime_breakdown.curve_selection.profile.value if regime_breakdown.curve_selection else "UNKNOWN"
        trade["metadata"]["base_cost_bps"] = regime_breakdown.total_base_cost_bps
        trade["metadata"]["adjusted_cost_bps"] = regime_breakdown.total_adjusted_cost_bps
        if regime_breakdown.adaptive_decision:
            trade["metadata"]["adaptive_execution_decision"] = regime_breakdown.adaptive_decision.decision.value
        trade["metadata"]["regime_cost_warnings"] = regime_breakdown.warnings
    return trade

def attach_regime_costs_to_backtest_result(result: Dict[str, Any], snapshots: Optional[List[CostRegimeSnapshot]] = None) -> Dict[str, Any]:
    result["metadata"] = result.get("metadata", {})
    if snapshots:
        # Just a high-level summary of regimes seen
        counts = {}
        for s in snapshots:
            c = s.combined_regime.value
            counts[c] = counts.get(c, 0) + 1
        result["metadata"]["regime_distribution"] = counts
    return result

def backtest_regime_cost_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    meta = result.get("metadata", {})
    return {
        "regime_distribution": meta.get("regime_distribution", {})
    }

def backtest_regime_cost_warnings(result: Dict[str, Any]) -> List[str]:
    w = []
    meta = result.get("metadata", {})
    dist = meta.get("regime_distribution", {})
    if dist.get("HIGH_RISK", 0) > 0 or dist.get("BLOCKED", 0) > 0:
        w.append("Backtest contains trades in HIGH_RISK or BLOCKED regimes.")
    return w
