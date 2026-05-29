from typing import Any

from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import RegimeDiagnosticsInterpretation

def _build_generic_interpretation(item: dict[str, Any], kind: str, name: str) -> RegimeDiagnosticsInterpretation:
    i = RegimeDiagnosticsInterpretation()
    i.symbol = item.get("symbol")
    i.source_diagnostic_kind = kind
    i.interpretation_name = name
    i.interpretation_text = f"Heuristic interpretation of {kind}. This is not a strategy recommendation."
    if "high churn" in i.interpretation_text.lower():
        i.interpretation_text = "High churn observed. This is a research finding, not a trade alert."
    if "low stability" in i.interpretation_text.lower():
        i.interpretation_text = "Low stability observed. This is a research finding, not a strategy on/off switch."
    return i

def interpret_transition_matrix(matrix: dict[str, Any]) -> RegimeDiagnosticsInterpretation:
    return _build_generic_interpretation(matrix, "TRANSITION_MATRIX", "Transition Matrix Interpretation")

def interpret_persistence_profile(profile: dict[str, Any]) -> RegimeDiagnosticsInterpretation:
    return _build_generic_interpretation(profile, "PERSISTENCE_PROFILE", "Persistence Profile Interpretation")

def interpret_churn_diagnostic(diagnostic: dict[str, Any]) -> RegimeDiagnosticsInterpretation:
    return _build_generic_interpretation(diagnostic, "CHURN_DIAGNOSTIC", "Churn Diagnostic Interpretation")

def interpret_stability_diagnostic(diagnostic: dict[str, Any]) -> RegimeDiagnosticsInterpretation:
    return _build_generic_interpretation(diagnostic, "STABILITY_DIAGNOSTICS", "Stability Diagnostic Interpretation")

def build_diagnostics_interpretations(payloads: dict[str, list[dict[str, Any]]]) -> list[RegimeDiagnosticsInterpretation]:
    ints = []
    for m in payloads.get("transition_matrices", []): ints.append(interpret_transition_matrix(m))
    for p in payloads.get("persistence_profiles", []): ints.append(interpret_persistence_profile(p))
    for c in payloads.get("churn_diagnostics", []): ints.append(interpret_churn_diagnostic(c))
    for s in payloads.get("stability_diagnostics", []): ints.append(interpret_stability_diagnostic(s))
    return ints

def validate_diagnostics_interpretations(items: list[RegimeDiagnosticsInterpretation]) -> list[str]:
    errs = []
    for i in items:
        if not i.research_metadata_only: errs.append(f"Interpretation {i.interpretation_id} research_metadata_only must be true")
        if i.investment_advice: errs.append(f"Interpretation {i.interpretation_id} investment_advice must be false")
        if i.produces_trade_signal: errs.append(f"Interpretation {i.interpretation_id} produces_trade_signal must be false")
        if i.produces_order_decision: errs.append(f"Interpretation {i.interpretation_id} produces_order_decision must be false")
        if i.produces_portfolio_weights: errs.append(f"Interpretation {i.interpretation_id} produces_portfolio_weights must be false")
        if "trade alert" in i.interpretation_text.lower() and "not a trade alert" not in i.interpretation_text.lower():
            errs.append("Invalid 'trade alert' phrasing.")
        if "strategy on/off" in i.interpretation_text.lower() and "not a strategy" not in i.interpretation_text.lower():
            errs.append("Invalid 'strategy on/off' phrasing.")
    return errs

def diagnostics_interpretations_to_text(items: list[RegimeDiagnosticsInterpretation], limit: int = 300) -> str:
    lines = [f"Interpretations ({len(items)}):"]
    for i in items[:5]:
        lines.append(f"- {i.interpretation_name} for {i.symbol}")
    return "\n".join(lines)[:limit]
