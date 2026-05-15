from typing import Any
from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation, SymbolRegimeAlignment, RegimeTransitionSignal
from usa_signal_bot.core.enums import RegimeAlignmentStatus, RegimeTransitionRisk

def attach_regime_map_to_paper_order(order: dict[str, Any], confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None = None) -> dict[str, Any]:
    out = dict(order)
    if "metadata" not in out:
        out["metadata"] = {}

    out["metadata"]["regime_confirmation"] = confirmation.status.value if confirmation else "UNKNOWN"
    out["metadata"]["regime_alignment"] = alignment.status.value if alignment else "UNKNOWN"
    return out

def attach_regime_map_to_paper_fill(fill: dict[str, Any], confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None = None) -> dict[str, Any]:
    out = dict(fill)
    if "metadata" not in out:
        out["metadata"] = {}

    out["metadata"]["regime_confirmation"] = confirmation.status.value if confirmation else "UNKNOWN"
    return out

def paper_regime_map_summary(orders_or_fills: list[dict[str, Any]]) -> dict[str, Any]:
    conflicted = 0
    total = len(orders_or_fills)
    for item in orders_or_fills:
        if item.get("metadata", {}).get("regime_alignment") in [RegimeAlignmentStatus.CONFLICTED.value, RegimeAlignmentStatus.DIVERGENT.value]:
            conflicted += 1

    return {
        "total_items": total,
        "conflicted_alignment_count": conflicted
    }

def paper_order_allowed_by_regime_map(alignment: SymbolRegimeAlignment | None, transitions: list[RegimeTransitionSignal] | None = None) -> bool:
    if alignment and alignment.status == RegimeAlignmentStatus.CONFLICTED:
        return False

    if transitions:
        from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
        if aggregate_transition_risk(transitions) == RegimeTransitionRisk.CRITICAL:
            return False

    return True
