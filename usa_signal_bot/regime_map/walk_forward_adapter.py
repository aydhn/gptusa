from typing import Any
from usa_signal_bot.regime_map.regime_map_models import RegimeMapReview
from usa_signal_bot.core.enums import RegimeConfirmationStatus

def attach_regime_map_to_walk_forward_result(result: dict[str, Any], reviews_by_window: dict[str, RegimeMapReview] | None = None) -> dict[str, Any]:
    enriched = result.copy()
    if not reviews_by_window:
        return enriched

    # Walk forward results usually have a 'windows' list
    windows = enriched.get("windows", [])
    for window in windows:
        window_id = window.get("window_id")
        if window_id and window_id in reviews_by_window:
            review = reviews_by_window[window_id]
            window_meta = window.get("metadata", {})

            if review.cross_sectional_map:
                window_meta["cross_sectional_regime"] = review.cross_sectional_map.cross_sectional_regime.value

            window["metadata"] = window_meta

    enriched["windows"] = windows

    # Add overall stability
    stability = classify_walk_forward_regime_stability(enriched)
    enriched_meta = enriched.get("metadata", {})
    enriched_meta["regime_stability"] = stability.value
    enriched["metadata"] = enriched_meta

    return enriched

def classify_walk_forward_regime_stability(result: dict[str, Any]) -> RegimeConfirmationStatus:
    # A heuristic: if cross sectional regime changes wildly across windows, it's divergent
    windows = result.get("windows", [])
    if not windows:
        return RegimeConfirmationStatus.INSUFFICIENT_DATA

    regimes = set()
    for w in windows:
        r = w.get("metadata", {}).get("cross_sectional_regime")
        if r:
            regimes.add(r)

    if not regimes:
        return RegimeConfirmationStatus.INSUFFICIENT_DATA

    if len(regimes) == 1:
        return RegimeConfirmationStatus.CONFIRMED
    elif len(regimes) <= 3:
        return RegimeConfirmationStatus.PARTIAL
    else:
        return RegimeConfirmationStatus.DIVERGENT

def walk_forward_regime_map_summary(result: dict[str, Any]) -> dict[str, Any]:
    meta = result.get("metadata", {})
    return {
        "regime_stability": meta.get("regime_stability", "UNKNOWN")
    }

def walk_forward_regime_transition_warnings(result: dict[str, Any]) -> list[str]:
    # E.g. Warn if out of sample window is in a different regime than in-sample
    return []
