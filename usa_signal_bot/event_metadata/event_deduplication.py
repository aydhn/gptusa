
from typing import List, Tuple, Dict, Any
from usa_signal_bot.event_metadata.phase111_models import UnifiedMarketEvent

def event_deduplication_key(event: UnifiedMarketEvent) -> str:
    return f"{event.event_kind}_{event.symbol}_{event.country}_{event.event_name}_{event.scheduled_at_utc}"

def deduplicate_events(events: List[UnifiedMarketEvent]) -> Tuple[List[UnifiedMarketEvent], List[UnifiedMarketEvent]]:
    seen = set()
    unique = []
    duplicates = []
    for e in events:
        key = event_deduplication_key(e)
        if key in seen:
            duplicates.append(e)
        else:
            seen.add(key)
            unique.append(e)
    return unique, duplicates

def find_duplicate_events(events: List[UnifiedMarketEvent]) -> List[UnifiedMarketEvent]:
    _, duplicates = deduplicate_events(events)
    return duplicates

def event_deduplication_summary(events: List[UnifiedMarketEvent]) -> Dict[str, Any]:
    _, duplicates = deduplicate_events(events)
    return {"total": len(events), "duplicates": len(duplicates)}

def event_deduplication_to_text(duplicates: List[UnifiedMarketEvent], limit: int = 100) -> str:
    return f"Found {len(duplicates)} duplicate events."
