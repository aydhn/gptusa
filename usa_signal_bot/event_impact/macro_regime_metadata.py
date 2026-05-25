
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import MacroRegimeMetadataLabel, EventImpactConfidence
from usa_signal_bot.event_impact.phase112_models import MacroRegimeMetadata, create_macro_regime_id, _now

def infer_macro_regime_label(payload: Dict[str, Any]) -> MacroRegimeMetadataLabel:
    return MacroRegimeMetadataLabel.UNKNOWN_CONTEXT

def macro_regime_confidence(payload: Dict[str, Any]) -> EventImpactConfidence:
    return EventImpactConfidence.MEDIUM

def build_macro_regime_metadata(events: Optional[List[Dict[str, Any]]] = None, macro_series_payloads: Optional[List[Dict[str, Any]]] = None) -> List[MacroRegimeMetadata]:
    evs = events or []
    if not evs:
        return []

    return [MacroRegimeMetadata(
        regime_id=create_macro_regime_id(),
        created_at_utc=_now(),
        label=infer_macro_regime_label(evs[0]),
        source_event_ids=[e.get("event_id", "") for e in evs],
        macro_series_ids=[],
        confidence=macro_regime_confidence(evs[0]),
        confidence_score=50.0,
        description="Regime context metadata.",
        research_context_only=True,
        produces_trade_signal=False,
        produces_order_decision=False
    )]

def macro_regime_metadata_summary(items: List[MacroRegimeMetadata]) -> Dict[str, Any]:
    return {"total": len(items)}

def macro_regime_metadata_to_text(items: List[MacroRegimeMetadata], limit: int = 200) -> str:
    return f"{len(items)} regimes built."
