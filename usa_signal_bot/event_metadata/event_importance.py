
from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import MarketEventKind, MarketEventImportance
from usa_signal_bot.event_metadata.phase111_models import UnifiedMarketEvent

def infer_event_importance(event_kind: MarketEventKind, event_name: Optional[str] = None, symbol: Optional[str] = None) -> MarketEventImportance:
    if event_kind == MarketEventKind.FED_EVENT:
        return MarketEventImportance.HIGH
    if event_kind == MarketEventKind.EARNINGS:
        return MarketEventImportance.HIGH
    if event_kind == MarketEventKind.ECONOMIC_RELEASE:
        if event_name and ("CPI" in event_name or "Payrolls" in event_name):
            return MarketEventImportance.HIGH
        return MarketEventImportance.MEDIUM
    if event_kind == MarketEventKind.NEWS_METADATA:
        return MarketEventImportance.INFORMATIONAL
    return MarketEventImportance.UNKNOWN

def importance_rank(importance: MarketEventImportance) -> int:
    ranks = {
        MarketEventImportance.HIGH: 4,
        MarketEventImportance.MEDIUM: 3,
        MarketEventImportance.LOW: 2,
        MarketEventImportance.INFORMATIONAL: 1,
        MarketEventImportance.UNKNOWN: 0
    }
    return ranks.get(importance, 0)

def event_importance_summary(events: List[UnifiedMarketEvent]) -> Dict[str, Any]:
    return {"total": len(events)}

def event_importance_to_text(importance: MarketEventImportance) -> str:
    return f"Importance: {importance.value}"
