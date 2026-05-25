
from typing import Any, Dict, List
from usa_signal_bot.core.enums import EventImpactCategory
from usa_signal_bot.event_impact.phase112_models import SymbolEventExposure, EventImpactTag, create_symbol_event_exposure_id, _now

def compute_symbol_event_exposure_score(tags: List[EventImpactTag]) -> float:
    return min(100.0, len(tags) * 10.0)

def symbol_event_exposure_label(score: float) -> str:
    if score > 75: return "HIGH_EXPOSURE"
    if score > 25: return "MEDIUM_EXPOSURE"
    return "LOW_EXPOSURE"

def build_symbol_event_exposure(symbol: str, impact_tags: List[EventImpactTag]) -> SymbolEventExposure:
    my_tags = [t for t in impact_tags if t.symbol == symbol or not t.symbol]
    high = sum(1 for t in my_tags if "HIGH" in t.impact_category.value)
    med = sum(1 for t in my_tags if "MEDIUM" in t.impact_category.value)
    low = sum(1 for t in my_tags if "LOW" in t.impact_category.value or "INFORMATIONAL" in t.impact_category.value or "CONTEXT" in t.impact_category.value)

    score = compute_symbol_event_exposure_score(my_tags)

    return SymbolEventExposure(
        exposure_id=create_symbol_event_exposure_id(),
        created_at_utc=_now(),
        symbol=symbol,
        event_ids=[t.impact_tag_id for t in my_tags],
        high_impact_event_count=high,
        medium_impact_event_count=med,
        low_impact_event_count=low,
        nearest_event_at_utc=None,
        exposure_score=score,
        exposure_label=symbol_event_exposure_label(score),
        research_context_only=True,
        produces_trade_signal=False,
        produces_order_decision=False
    )

def build_symbol_event_exposures(symbols: List[str], impact_tags: List[EventImpactTag]) -> List[SymbolEventExposure]:
    return [build_symbol_event_exposure(sym, impact_tags) for sym in symbols]

def symbol_event_exposure_summary(items: List[SymbolEventExposure]) -> Dict[str, Any]:
    return {"total": len(items)}

def symbol_event_exposure_to_text(items: List[SymbolEventExposure], limit: int = 200) -> str:
    return f"{len(items)} exposures built."
