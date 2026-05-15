from typing import Any
from usa_signal_bot.regime_map.regime_map_models import RegimeMapReview, RegimeTransitionSignal
from usa_signal_bot.core.enums import RegimeTransitionType, BreadthRegime, LiquidityMapRegime

def cost_robustness_hints_from_regime_map(review: RegimeMapReview) -> dict[str, Any]:
    hints = {
        "stress_scenarios": [],
        "warnings": []
    }

    if review.cross_sectional_map:
         if review.cross_sectional_map.breadth_regime == BreadthRegime.DETERIORATING:
             hints["stress_scenarios"].append({"type": "risk_off_stress", "multiplier": 1.5})
             hints["warnings"].append("Breadth deteriorating: suggest risk-off cost stress.")

    transitions = review.transition_signals
    if transitions:
        stress = transition_risk_stress_scenarios_hint(transitions)
        hints["stress_scenarios"].extend(stress)

    return hints

def transition_risk_stress_scenarios_hint(transitions: list[RegimeTransitionSignal]) -> list[dict[str, Any]]:
    scenarios = []
    types = [t.transition_type for t in transitions]

    if RegimeTransitionType.LIQUIDITY_NORMAL_TO_THIN in types:
         scenarios.append({"type": "liquidity_thinning_stress", "slippage_multiplier": 2.0})

    if RegimeTransitionType.LOW_VOL_TO_HIGH_VOL in types:
         scenarios.append({"type": "volatility_expansion_stress", "spread_multiplier": 1.5})

    return scenarios

def adjust_cost_fragility_with_regime_transition(assessment_payload: dict[str, Any], transitions: list[RegimeTransitionSignal]) -> dict[str, Any]:
    out = dict(assessment_payload)
    if not transitions:
        return out

    from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
    from usa_signal_bot.core.enums import RegimeTransitionRisk

    risk = aggregate_transition_risk(transitions)
    if risk in [RegimeTransitionRisk.HIGH, RegimeTransitionRisk.CRITICAL]:
        out["fragility_score"] = min(100.0, out.get("fragility_score", 0) + 20.0)
        if "warnings" not in out:
             out["warnings"] = []
        out["warnings"].append("Fragility score artificially increased due to high regime transition risk.")

    return out

def regime_map_robustness_adapter_summary_to_text(payload: dict[str, Any]) -> str:
    score = payload.get("fragility_score", 0)
    warnings = len(payload.get("warnings", []))
    return f"Robustness Adjusted Score: {score:.2f} | Warnings: {warnings}"
