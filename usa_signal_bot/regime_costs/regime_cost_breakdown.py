from typing import Optional, Dict, Any
from usa_signal_bot.core.enums import RegimeCostAdjustmentStatus
from usa_signal_bot.regime_costs.regime_cost_models import (
    CostRegimeSnapshot, RegimeCostCurveSelection, AdaptiveExecutionRealismDecision,
    RegimeAwareCostBreakdown, RegimeCostMultiplier, create_regime_aware_cost_breakdown_id, get_utc_now_str
)

def build_regime_aware_cost_breakdown(
    symbol: str,
    base_cost_breakdown: Optional[Dict[str, Any]],
    snapshot: CostRegimeSnapshot,
    selection: Optional[RegimeCostCurveSelection] = None,
    decision: Optional[AdaptiveExecutionRealismDecision] = None
) -> RegimeAwareCostBreakdown:
    warnings = []

    if not base_cost_breakdown:
        warnings.append("Base cost breakdown is missing. Cannot calculate full adjusted breakdown.")
        return RegimeAwareCostBreakdown(
            breakdown_id=create_regime_aware_cost_breakdown_id(symbol),
            symbol=symbol,
            created_at_utc=get_utc_now_str(),
            base_cost_breakdown=None,
            adjusted_cost_breakdown=None,
            regime_snapshot=snapshot,
            curve_selection=selection,
            adaptive_decision=decision,
            total_base_cost_bps=None,
            total_adjusted_cost_bps=None,
            adjustment_delta_bps=None,
            status=RegimeCostAdjustmentStatus.PARTIAL,
            warnings=warnings,
            errors=[],
            metadata={}
        )

    mult = selection.multiplier if selection and selection.multiplier else None

    if mult is None:
        warnings.append("No multiplier found in curve selection. Adjustments might be skipped.")
        adj_breakdown = base_cost_breakdown
        base_bps = base_cost_breakdown.get("total_cost_bps")
        adj_bps = base_bps
        delta = 0.0
        status = RegimeCostAdjustmentStatus.SKIPPED
    else:
        adj_breakdown = apply_regime_multiplier_to_cost_breakdown(base_cost_breakdown, mult)
        base_bps = base_cost_breakdown.get("total_cost_bps")
        adj_bps = adj_breakdown.get("total_cost_bps")
        delta = calculate_regime_cost_delta_bps(base_bps, adj_bps)
        status = RegimeCostAdjustmentStatus.APPLIED

    return RegimeAwareCostBreakdown(
        breakdown_id=create_regime_aware_cost_breakdown_id(symbol),
        symbol=symbol,
        created_at_utc=get_utc_now_str(),
        base_cost_breakdown=base_cost_breakdown,
        adjusted_cost_breakdown=adj_breakdown,
        regime_snapshot=snapshot,
        curve_selection=selection,
        adaptive_decision=decision,
        total_base_cost_bps=base_bps,
        total_adjusted_cost_bps=adj_bps,
        adjustment_delta_bps=delta,
        status=status,
        warnings=warnings,
        errors=[],
        metadata={}
    )

def apply_regime_multiplier_to_cost_breakdown(base_cost_breakdown: Dict[str, Any], multiplier: RegimeCostMultiplier) -> Dict[str, Any]:
    adj = dict(base_cost_breakdown)
    mult_val = multiplier.combined_multiplier

    # components like slippage and market impact are affected heavily by the combined multiplier
    for key in ["slippage_bps", "market_impact_bps", "spread_cost_bps"]:
        if key in adj and isinstance(adj[key], (int, float)):
            adj[key] = adj[key] * mult_val

    # Fees might be affected less or not at all, assuming constant here for safety

    # recompute total
    tot = 0.0
    for k, v in adj.items():
        if k != "total_cost_bps" and k.endswith("_bps") and isinstance(v, (int, float)):
            tot += v

    # Apply max cap
    if multiplier.max_cost_bps is not None and tot > multiplier.max_cost_bps:
        tot = multiplier.max_cost_bps

    adj["total_cost_bps"] = tot
    return adj

def calculate_regime_cost_delta_bps(base_cost_bps: Optional[float], adjusted_cost_bps: Optional[float]) -> Optional[float]:
    if base_cost_bps is None or adjusted_cost_bps is None:
        return None
    return adjusted_cost_bps - base_cost_bps

def regime_aware_cost_breakdown_to_text(result: RegimeAwareCostBreakdown) -> str:
    s = f"Breakdown for {result.symbol}: Base={result.total_base_cost_bps}bps, Adjusted={result.total_adjusted_cost_bps}bps"
    return s
