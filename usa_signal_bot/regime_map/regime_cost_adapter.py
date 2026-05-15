from typing import Any
from usa_signal_bot.regime_map.regime_map_models import (
    MultiTimeframeRegimeConfirmation,
    SymbolRegimeAlignment,
    RegimeTransitionSignal
)
from usa_signal_bot.core.enums import RegimeAlignmentStatus, RegimeTransitionRisk

def regime_cost_snapshot_from_regime_map_confirmation(confirmation: MultiTimeframeRegimeConfirmation, alignment: SymbolRegimeAlignment | None = None) -> dict[str, Any]:
    # Creates a payload that Phase 57 regime_cost might use as a hint
    payload = {
         "symbol": confirmation.symbol,
         "volatility_regime": confirmation.dominant_volatility_regime.value,
         "liquidity_regime": confirmation.dominant_liquidity_regime.value,
         "trend_regime": confirmation.dominant_trend_regime.value
    }

    if alignment:
        payload["alignment_status"] = alignment.status.value

    return payload

def adjust_regime_cost_decision_with_transition_risk(decision_payload: dict[str, Any], transitions: list[RegimeTransitionSignal]) -> dict[str, Any]:
    enriched = decision_payload.copy()
    if not transitions:
         return enriched

    risks = [t.risk for t in transitions]

    if RegimeTransitionRisk.CRITICAL in risks or RegimeTransitionRisk.HIGH in risks:
        # Hint to the cost model to be more conservative/stressed
        enriched["apply_transition_stress"] = True
        enriched["stress_factor"] = 1.5 if RegimeTransitionRisk.CRITICAL in risks else 1.2

    return enriched

def regime_map_cost_warnings(confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None, transitions: list[RegimeTransitionSignal] | None = None) -> list[str]:
    warnings = []

    if alignment and alignment.status in [RegimeAlignmentStatus.CONFLICTED, RegimeAlignmentStatus.DIVERGENT]:
        warnings.append("Cost model warning: Alignment is conflicted/divergent, slippage may be higher than estimated.")

    if transitions:
        risks = [t.risk for t in transitions]
        if RegimeTransitionRisk.CRITICAL in risks or RegimeTransitionRisk.HIGH in risks:
             warnings.append("Cost model warning: High transition risk detected, execution costs may spike unpredictably.")

    return warnings

def regime_map_cost_adapter_summary_to_text(payload: dict[str, Any]) -> str:
    parts = []
    if payload.get("apply_transition_stress"):
         parts.append(f"Applied stress factor {payload.get('stress_factor', 1.0)} due to transition risk.")
    return " ".join(parts) if parts else "No cost adjustments."
