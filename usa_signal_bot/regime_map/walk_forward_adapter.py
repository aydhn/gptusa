from typing import Any
from usa_signal_bot.regime_map.regime_map_models import RegimeMapReview
from usa_signal_bot.core.enums import RegimeConfirmationStatus

def attach_regime_map_to_walk_forward_result(result: dict[str, Any], reviews_by_window: dict[str, RegimeMapReview] | None = None) -> dict[str, Any]:
    out = dict(result)
    if "metadata" not in out:
        out["metadata"] = {}

    out["metadata"]["regime_map_attached"] = True

    # Store minimal info per window
    window_regimes = {}
    if reviews_by_window:
        for w_id, rev in reviews_by_window.items():
            reg = "UNKNOWN"
            if rev.cross_sectional_map:
                reg = rev.cross_sectional_map.cross_sectional_regime.value
            window_regimes[w_id] = reg

    out["metadata"]["window_regimes"] = window_regimes
    return out

def walk_forward_regime_map_summary(result: dict[str, Any]) -> dict[str, Any]:
    meta = result.get("metadata", {})
    return {
        "regime_attached": meta.get("regime_map_attached", False),
        "window_regimes": meta.get("window_regimes", {})
    }

def walk_forward_regime_transition_warnings(result: dict[str, Any]) -> list[str]:
    # Check if regimes flip wildly between windows
    meta = result.get("metadata", {})
    windows = meta.get("window_regimes", {})
    warnings = []

    regs = list(windows.values())
    for i in range(1, len(regs)):
        if regs[i] != regs[i-1] and regs[i-1] != "UNKNOWN":
            warnings.append(f"Regime transition across WF windows: {regs[i-1]} -> {regs[i]}")

    return warnings

def classify_walk_forward_regime_stability(result: dict[str, Any]) -> RegimeConfirmationStatus:
    meta = result.get("metadata", {})
    windows = meta.get("window_regimes", {})
    if not windows:
        return RegimeConfirmationStatus.INSUFFICIENT_DATA

    unique_regimes = set(windows.values()) - {"UNKNOWN"}
    if len(unique_regimes) <= 1:
        return RegimeConfirmationStatus.CONFIRMED
    elif len(unique_regimes) > 2:
        return RegimeConfirmationStatus.CONFLICTED
    else:
        return RegimeConfirmationStatus.DIVERGENT
