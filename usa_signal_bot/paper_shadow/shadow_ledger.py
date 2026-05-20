from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowLedgerEvent, ShadowRehearsalSession, create_shadow_ledger_event_id, get_utc_now_str
)
from usa_signal_bot.core.enums import ShadowLedgerEventType

def create_shadow_ledger_event(
    event_type: ShadowLedgerEventType,
    payload: Dict[str, Any],
    symbol: str | None = None,
    ref_id: str | None = None
) -> ShadowLedgerEvent:
    # Ensure no secrets in payload (simple check)
    clean_payload = {k: v for k, v in payload.items() if "secret" not in k.lower() and "key" not in k.lower()}

    return ShadowLedgerEvent(
        event_id=create_shadow_ledger_event_id(),
        created_at_utc=get_utc_now_str(),
        event_type=event_type,
        symbol=symbol,
        ref_id=ref_id,
        payload=clean_payload,
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def build_ledger_from_shadow_session(session: ShadowRehearsalSession) -> List[ShadowLedgerEvent]:
    return session.ledger_events

def append_shadow_ledger_event(events: List[ShadowLedgerEvent], event: ShadowLedgerEvent) -> List[ShadowLedgerEvent]:
    events.append(event)
    return events

def shadow_ledger_summary(events: List[ShadowLedgerEvent]) -> Dict[str, Any]:
    return {
        "count": len(events),
        "started": any(e.event_type == ShadowLedgerEventType.SESSION_STARTED for e in events),
        "completed": any(e.event_type == ShadowLedgerEventType.SESSION_COMPLETED for e in events)
    }

def shadow_ledger_to_text(events: List[ShadowLedgerEvent], limit: int = 100) -> str:
    s = shadow_ledger_summary(events)
    return f"ShadowLedger(count={s['count']})"
