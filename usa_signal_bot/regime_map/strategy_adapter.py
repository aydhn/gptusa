from typing import Any
from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation, SymbolRegimeAlignment, RegimeTransitionSignal
from usa_signal_bot.core.enums import RegimeAlignmentStatus, RegimeTransitionRisk

def attach_regime_confirmation_to_signal(signal: dict[str, Any], confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None = None, transitions: list[RegimeTransitionSignal] | None = None) -> dict[str, Any]:
    # Returns a new dict, avoids mutating original if possible, but deepcopy is better. For now simple dict update
    out = dict(signal)
    if "metadata" not in out:
        out["metadata"] = {}

    out["metadata"]["regime_confirmation_status"] = confirmation.status.value if confirmation else "UNKNOWN"
    out["metadata"]["regime_alignment"] = alignment.status.value if alignment else "UNKNOWN"

    if transitions:
         from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
         agg_risk = aggregate_transition_risk(transitions)
         out["metadata"]["transition_risk"] = agg_risk.value

    return out

def attach_regime_confirmation_to_candidate(candidate: dict[str, Any], confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None = None, transitions: list[RegimeTransitionSignal] | None = None) -> dict[str, Any]:
    out = dict(candidate)
    if "metadata" not in out:
        out["metadata"] = {}

    out["metadata"]["regime_confirmation"] = confirmation.status.value if confirmation else "UNKNOWN"
    out["metadata"]["regime_alignment"] = alignment.status.value if alignment else "UNKNOWN"

    penalty = regime_alignment_rank_penalty(alignment, transitions)
    if penalty > 0:
         out["metadata"]["regime_rank_penalty"] = penalty
         # Assume we have a score field
         if "score" in out:
              out["score"] -= penalty

    out = suppress_candidate_if_regime_conflicted(out, alignment, transitions)
    return out

def regime_alignment_rank_penalty(alignment: SymbolRegimeAlignment | None, transitions: list[RegimeTransitionSignal] | None = None) -> float:
    penalty = 0.0
    if alignment:
        if alignment.status == RegimeAlignmentStatus.CONFLICTED:
             penalty += 20.0
        elif alignment.status == RegimeAlignmentStatus.DIVERGENT:
             penalty += 10.0

    if transitions:
        from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
        risk = aggregate_transition_risk(transitions)
        if risk == RegimeTransitionRisk.CRITICAL:
             penalty += 30.0
        elif risk == RegimeTransitionRisk.HIGH:
             penalty += 15.0

    return penalty

def suppress_candidate_if_regime_conflicted(candidate: dict[str, Any], alignment: SymbolRegimeAlignment | None, transitions: list[RegimeTransitionSignal] | None = None) -> dict[str, Any]:
    if alignment and alignment.status == RegimeAlignmentStatus.CONFLICTED:
         candidate["metadata"]["suppressed"] = True
         candidate["metadata"]["suppression_reason"] = "REGIME_CONFLICT"

    if transitions:
         from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
         risk = aggregate_transition_risk(transitions)
         if risk == RegimeTransitionRisk.CRITICAL:
              candidate["metadata"]["suppressed"] = True
              candidate["metadata"]["suppression_reason"] = "CRITICAL_TRANSITION_RISK"

    return candidate

def candidate_regime_map_summary(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    suppressed = sum(1 for c in candidates if c.get("metadata", {}).get("suppressed"))
    return {
        "total_candidates": len(candidates),
        "suppressed_by_regime": suppressed
    }
