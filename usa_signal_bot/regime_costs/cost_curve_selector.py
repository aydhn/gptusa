from typing import Optional, Any
from usa_signal_bot.core.enums import RegimeCostCurveProfile, CombinedCostRegime
from usa_signal_bot.regime_costs.regime_cost_models import (
    CostRegimeSnapshot, RegimeCostCurveSelection, RegimeCostMultiplier,
    create_regime_cost_curve_selection_id, get_utc_now_str
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_regime_cost_multiplier

def select_cost_curve_profile(snapshot: CostRegimeSnapshot) -> RegimeCostCurveProfile:
    if snapshot.combined_regime == CombinedCostRegime.BLOCKED:
        return RegimeCostCurveProfile.BLOCKED
    if snapshot.combined_regime == CombinedCostRegime.HIGH_RISK:
        return RegimeCostCurveProfile.EXTREME
    if snapshot.combined_regime == CombinedCostRegime.STRESSED:
        return RegimeCostCurveProfile.STRESSED
    if snapshot.combined_regime == CombinedCostRegime.CONSERVATIVE or snapshot.combined_regime == CombinedCostRegime.INSUFFICIENT_DATA:
        return RegimeCostCurveProfile.CONSERVATIVE

    return RegimeCostCurveProfile.BASELINE

def select_slippage_curve_for_regime(symbol: str, snapshot: CostRegimeSnapshot, base_curve: Optional[Any] = None) -> RegimeCostCurveSelection:
    profile = select_cost_curve_profile(snapshot)
    multiplier = build_regime_cost_multiplier(symbol, snapshot)

    # In a real system, we'd look up a specific curve by ID based on profile.
    # Here we just use a heuristic string.
    selected_curve_id = f"curve_{profile.value.lower()}"
    base_id = base_curve.curve_id if base_curve and hasattr(base_curve, "curve_id") else "default_base_curve"

    return RegimeCostCurveSelection(
        selection_id=create_regime_cost_curve_selection_id(symbol),
        symbol=symbol,
        created_at_utc=get_utc_now_str(),
        profile=profile,
        selected_curve_id=selected_curve_id,
        base_curve_id=base_id,
        regime_snapshot=snapshot,
        multiplier=multiplier,
        reason=f"Profile selected based on combined regime {snapshot.combined_regime.value}",
        warnings=[],
        errors=[],
        metadata={}
    )

def adjust_slippage_curve_for_regime(base_curve: Any, multiplier: RegimeCostMultiplier) -> Any:
    # Existing SlippageCurve may not be loaded directly without circular imports or pathing issues.
    # We return the base curve modified if possible, or just the base curve as is, representing heuristic adjustment.
    return base_curve

def curve_profile_to_default_multiplier(profile: RegimeCostCurveProfile) -> float:
    mapping = {
        RegimeCostCurveProfile.BASELINE: 1.0,
        RegimeCostCurveProfile.LIQUID: 0.8,
        RegimeCostCurveProfile.CONSERVATIVE: 1.5,
        RegimeCostCurveProfile.STRESSED: 2.5,
        RegimeCostCurveProfile.EXTREME: 4.0,
        RegimeCostCurveProfile.BLOCKED: 10.0,
        RegimeCostCurveProfile.UNKNOWN: 1.0,
    }
    return mapping.get(profile, 1.0)

def cost_curve_selection_to_text(selection: RegimeCostCurveSelection) -> str:
    return f"Curve Selection for {selection.symbol}: {selection.profile.value} (Curve ID: {selection.selected_curve_id})"
