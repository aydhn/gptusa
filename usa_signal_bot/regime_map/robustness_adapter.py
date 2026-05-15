from typing import Any
from usa_signal_bot.regime_map.regime_map_models import RegimeMapReview, RegimeTransitionSignal
from usa_signal_bot.core.enums import RegimeTransitionType

def cost_robustness_hints_from_regime_map(review: RegimeMapReview) -> dict[str, Any]:
    hints = {}
    if review.cross_sectional_map:
        hints["breadth_regime"] = review.cross_sectional_map.breadth_regime.value
        hints["dispersion_score"] = review.cross_sectional_map.dispersion_score

    return hints

def transition_risk_stress_scenarios_hint(transitions: list[RegimeTransitionSignal]) -> list[dict[str, Any]]:
    scenarios = []
    for t in transitions:
        if t.transition_type == RegimeTransitionType.BREADTH_RISK_ON_TO_OFF:
             scenarios.append({"name": "Risk-Off Breadth Stress", "slippage_multiplier": 2.0})
        elif t.transition_type == RegimeTransitionType.LIQUIDITY_NORMAL_TO_THIN:
             scenarios.append({"name": "Liquidity Thinning Stress", "volume_limit_pct": 0.5})
        elif t.transition_type == RegimeTransitionType.LOW_VOL_TO_HIGH_VOL:
             scenarios.append({"name": "Volatility Expansion Stress", "slippage_multiplier": 1.5})
    return scenarios

def adjust_cost_fragility_with_regime_transition(assessment_payload: dict[str, Any], transitions: list[RegimeTransitionSignal]) -> dict[str, Any]:
    enriched = assessment_payload.copy()
    scenarios = transition_risk_stress_scenarios_hint(transitions)
    if scenarios:
        existing_scenarios = enriched.get("recommended_stress_scenarios", [])
        existing_scenarios.extend(scenarios)
        enriched["recommended_stress_scenarios"] = existing_scenarios
        enriched["fragility_warning"] = "Regime transition risk indicates higher likelihood of cost fragility."
    return enriched

def regime_map_robustness_adapter_summary_to_text(payload: dict[str, Any]) -> str:
    scenarios = payload.get("recommended_stress_scenarios", [])
    if scenarios:
        names = [s.get("name", "Unknown") for s in scenarios]
        return f"Added Stress Scenarios: {', '.join(names)}"
    return "No robustness adjustments."
