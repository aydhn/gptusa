from typing import Any
from usa_signal_bot.regime_map.regime_map_models import (
    MultiTimeframeRegimeConfirmation,
    SymbolRegimeAlignment,
    RegimeTransitionSignal
)
from usa_signal_bot.core.enums import RegimeAlignmentStatus, RegimeTransitionRisk

def attach_regime_map_to_paper_order(order: dict[str, Any], confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None = None) -> dict[str, Any]:
    enriched = order.copy()
    metadata = enriched.get("metadata", {})

    if confirmation:
        metadata["regime_confirmation_status"] = confirmation.status.value

    if alignment:
        metadata["regime_alignment_status"] = alignment.status.value

    enriched["metadata"] = metadata
    return enriched

def attach_regime_map_to_paper_fill(fill: dict[str, Any], confirmation: MultiTimeframeRegimeConfirmation | None, alignment: SymbolRegimeAlignment | None = None) -> dict[str, Any]:
    # Similar to order, just copy metadata to the fill record
    enriched = fill.copy()
    metadata = enriched.get("metadata", {})

    if confirmation:
        metadata["regime_confirmation_status"] = confirmation.status.value

    if alignment:
         metadata["regime_alignment_status"] = alignment.status.value

    enriched["metadata"] = metadata
    return enriched

def paper_order_allowed_by_regime_map(alignment: SymbolRegimeAlignment | None, transitions: list[RegimeTransitionSignal] | None = None) -> bool:
    # A paper order might be skipped if regime alignment is terribly conflicted
    # or risk is critical. This is for local paper trading only, not real broker.
    if alignment and alignment.status == RegimeAlignmentStatus.CONFLICTED:
        return False

    if transitions:
        if any(t.risk == RegimeTransitionRisk.CRITICAL for t in transitions):
             return False

    return True

def paper_regime_map_summary(orders_or_fills: list[dict[str, Any]]) -> dict[str, Any]:
    conflicted = 0
    for item in orders_or_fills:
         if item.get("metadata", {}).get("regime_alignment_status") == "CONFLICTED":
             conflicted += 1

    return {
        "total_items": len(orders_or_fills),
        "conflicted_alignment_count": conflicted
    }
