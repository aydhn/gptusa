from typing import Any
from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation, SymbolRegimeAlignment, RegimeTransitionSignal
from usa_signal_bot.core.enums import RegimeAlignmentStatus, RegimeTransitionRisk

def regime_cost_snapshot_from_regime_map_confirmation(confirmation: MultiTimeframeRegimeConfirmation, alignment: SymbolRegimeAlignment | None = None) -> dict[str, Any]:
    # Phase 57 uses simple dicts for cost evaluation
    return {
        "trend_regime": confirmation.dominant_trend_regime.value,
        "volatility_regime": confirmation.dominant_volatility_regime.value,
        "liquidity_regime": confirmation.dominant_liquidity_regime.value,
        "alignment_status": alignment.status.value if alignment else "UNKNOWN"
    }

def adjust_regime_cost_decision_with_transition_risk(decision_payload: dict[str, Any], transitions: list[RegimeTransitionSignal]) -> dict[str, Any]:
    out = dict(decision_payload)
    if not transitions:
        return out

    from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
    agg_risk = aggregate_transition_risk(transitions)

    if agg_risk in [RegimeTransitionRisk.HIGH, RegimeTransitionRisk.CRITICAL]:
         out["decision"] = "STRESSED_COST_APPLIED"
         out["reason"] = f"Transition risk is {agg_risk.value}"

    return out

def regime_map_cost_warnings(confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None, transitions: list[RegimeTransitionSignal] | None = None) -> list[str]:
    warnings = []
    if alignment and alignment.status in [RegimeAlignmentStatus.CONFLICTED, RegimeAlignmentStatus.DIVERGENT]:
        warnings.append("Cost realism may be underestimated due to regime conflict.")

    if transitions:
        from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
        if aggregate_transition_risk(transitions) in [RegimeTransitionRisk.HIGH, RegimeTransitionRisk.CRITICAL]:
             warnings.append("High transition risk detected, apply conservative cost estimates.")

    return warnings

def regime_map_cost_adapter_summary_to_text(payload: dict[str, Any]) -> str:
    return f"Regime Cost Adapter: Decision={payload.get('decision', 'N/A')} Reason={payload.get('reason', 'N/A')}"
