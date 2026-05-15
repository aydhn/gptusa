from typing import Any
from usa_signal_bot.regime_map.regime_map_models import RegimeMapReview
from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk

def attach_regime_map_to_backtest_result(result: dict[str, Any], review: RegimeMapReview | None = None) -> dict[str, Any]:
    enriched = result.copy()
    metadata = enriched.get("metadata", {})

    if review:
        if review.cross_sectional_map:
            metadata["cross_sectional_regime"] = review.cross_sectional_map.cross_sectional_regime.value
            metadata["breadth_regime"] = review.cross_sectional_map.breadth_regime.value

        if review.transition_signals:
            agg_risk = aggregate_transition_risk(review.transition_signals)
            metadata["regime_transition_risk"] = agg_risk.value

        # Count alignment issues
        conflicted = sum(1 for a in review.alignments if a.status.value == "CONFLICTED")
        warnings = len(review.warnings)

        metadata["conflicted_alignment_count"] = conflicted
        metadata["regime_warning_count"] = warnings

    enriched["metadata"] = metadata
    return enriched

def backtest_regime_map_summary(result: dict[str, Any]) -> dict[str, Any]:
    meta = result.get("metadata", {})
    return {
        "cross_sectional_regime": meta.get("cross_sectional_regime", "UNKNOWN"),
        "regime_transition_risk": meta.get("regime_transition_risk", "UNKNOWN"),
        "conflicted_alignment_count": meta.get("conflicted_alignment_count", 0),
        "regime_warning_count": meta.get("regime_warning_count", 0)
    }

def backtest_regime_transition_warnings(result: dict[str, Any]) -> list[str]:
    meta = result.get("metadata", {})
    risk = meta.get("regime_transition_risk")
    warnings = []
    if risk in ["HIGH", "CRITICAL"]:
         warnings.append(f"Backtest executed during {risk} regime transition risk.")
    return warnings

def backtest_regime_conditioned_metrics_placeholder(result: dict[str, Any]) -> dict[str, Any]:
    # Placeholder for Phase 59 (Regime-conditioned strategy selection)
    return {}
