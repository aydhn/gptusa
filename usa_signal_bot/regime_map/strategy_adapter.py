from typing import Any
from usa_signal_bot.regime_map.regime_map_models import (
    MultiTimeframeRegimeConfirmation,
    SymbolRegimeAlignment,
    RegimeTransitionSignal
)
from usa_signal_bot.core.enums import RegimeAlignmentStatus, RegimeTransitionRisk

def attach_regime_confirmation_to_signal(signal: dict[str, Any], confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None = None, transitions: list[RegimeTransitionSignal] | None = None) -> dict[str, Any]:
    enriched = signal.copy()
    metadata = enriched.get("metadata", {})

    if confirmation:
        metadata["regime_confirmation_status"] = confirmation.status.value
        metadata["dominant_trend_regime"] = confirmation.dominant_trend_regime.value
        metadata["dominant_volatility_regime"] = confirmation.dominant_volatility_regime.value

    if alignment:
        metadata["regime_alignment_status"] = alignment.status.value
        if alignment.alignment_score is not None:
             metadata["regime_alignment_score"] = alignment.alignment_score

    if transitions:
        types = [t.transition_type.value for t in transitions]
        metadata["regime_transitions"] = types

    enriched["metadata"] = metadata
    return enriched

def attach_regime_confirmation_to_candidate(candidate: dict[str, Any], confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None = None, transitions: list[RegimeTransitionSignal] | None = None) -> dict[str, Any]:
    enriched = candidate.copy()
    metadata = enriched.get("metadata", {})

    if confirmation:
        metadata["regime_confirmation_status"] = confirmation.status.value
        metadata["dominant_trend_regime"] = confirmation.dominant_trend_regime.value

    if alignment:
        metadata["regime_alignment_status"] = alignment.status.value

    if transitions:
         metadata["regime_transitions"] = [t.transition_type.value for t in transitions]

    enriched["metadata"] = metadata
    return enriched

def regime_alignment_rank_penalty(alignment: SymbolRegimeAlignment | None, transitions: list[RegimeTransitionSignal] | None = None) -> float:
    penalty = 0.0
    if alignment:
        if alignment.status == RegimeAlignmentStatus.DIVERGENT:
            penalty += 20.0
        elif alignment.status == RegimeAlignmentStatus.CONFLICTED:
            penalty += 40.0

    if transitions:
        # Highest risk transition dictates penalty
        risks = [t.risk for t in transitions]
        if RegimeTransitionRisk.CRITICAL in risks:
             penalty += 50.0
        elif RegimeTransitionRisk.HIGH in risks:
             penalty += 30.0
        elif RegimeTransitionRisk.MODERATE in risks:
             penalty += 10.0

    return penalty

def suppress_candidate_if_regime_conflicted(candidate: dict[str, Any], alignment: SymbolRegimeAlignment | None, transitions: list[RegimeTransitionSignal] | None = None) -> dict[str, Any]:
    # Never change signal direction, just add metadata
    enriched = candidate.copy()
    metadata = enriched.get("metadata", {})

    suppress = False
    reasons = []

    if alignment and alignment.status == RegimeAlignmentStatus.CONFLICTED:
        suppress = True
        reasons.append("Conflicted regime alignment")

    if transitions and any(t.risk == RegimeTransitionRisk.CRITICAL for t in transitions):
        suppress = True
        reasons.append("Critical regime transition risk")

    if suppress:
         metadata["regime_map_suppression"] = True
         metadata["regime_map_suppression_reasons"] = reasons

    enriched["metadata"] = metadata
    return enriched

def candidate_regime_map_summary(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    suppressed = 0
    conflicted = 0

    for c in candidates:
        meta = c.get("metadata", {})
        if meta.get("regime_map_suppression"):
            suppressed += 1
        if meta.get("regime_alignment_status") == RegimeAlignmentStatus.CONFLICTED.value:
            conflicted += 1

    return {
        "total_candidates": len(candidates),
        "suppressed_by_regime_map": suppressed,
        "conflicted_alignment": conflicted
    }
