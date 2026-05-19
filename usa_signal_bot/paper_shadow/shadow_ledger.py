from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowLedgerEvent,
    ShadowRehearsalSession,
    create_shadow_ledger_event_id
)
from usa_signal_bot.core.enums import ShadowLedgerEventType, ShadowSessionStatus

def create_shadow_ledger_event(event_type: ShadowLedgerEventType, payload: dict[str, Any], symbol: str | None = None, ref_id: str | None = None) -> ShadowLedgerEvent:
    safe_payload = _sanitize_payload(payload)
    return ShadowLedgerEvent(
        event_id=create_shadow_ledger_event_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        event_type=event_type,
        payload=safe_payload,
        safety_flags=[],
        warnings=[],
        errors=[],
        symbol=symbol,
        ref_id=ref_id
    )

def _sanitize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    safe = {}
    for k, v in payload.items():
        k_lower = str(k).lower()
        if any(bad in k_lower for bad in ["secret", "token", "password", "key", "broker", "live_order"]):
            continue
        safe[k] = v
    return safe

def build_ledger_from_shadow_session(session: ShadowRehearsalSession) -> list[ShadowLedgerEvent]:
    events = []
    events.append(create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {"session_id": session.session_id}, ref_id=session.session_id))

    for sig in session.signals:
        events.append(create_shadow_ledger_event(ShadowLedgerEventType.SIGNAL_PREVIEWED, {"side": sig.side, "score": sig.score}, symbol=sig.symbol, ref_id=sig.signal_id))

    for intent in session.order_intents:
        events.append(create_shadow_ledger_event(ShadowLedgerEventType.ORDER_INTENT_CREATED, {"side": intent.side, "quantity": intent.quantity}, symbol=intent.symbol, ref_id=intent.intent_id))

    for fill in session.fills:
        events.append(create_shadow_ledger_event(ShadowLedgerEventType.FILL_SIMULATED, {"side": fill.side, "quantity": fill.filled_quantity, "price": fill.fill_price}, symbol=fill.symbol, ref_id=fill.fill_id))

    if session.status in [ShadowSessionStatus.COMPLETED, ShadowSessionStatus.FAILED, ShadowSessionStatus.BLOCKED]:
         events.append(create_shadow_ledger_event(ShadowLedgerEventType.SESSION_COMPLETED, {"session_id": session.session_id, "status": session.status.value}, ref_id=session.session_id))

    return events

def append_shadow_ledger_event(events: list[ShadowLedgerEvent], event: ShadowLedgerEvent) -> list[ShadowLedgerEvent]:
    events.append(event)
    return events

def shadow_ledger_summary(events: list[ShadowLedgerEvent]) -> dict[str, Any]:
    return {
        "count": len(events),
        "types": {e_type.name: sum(1 for e in events if e.event_type == e_type) for e_type in ShadowLedgerEventType}
    }

def shadow_ledger_to_text(events: list[ShadowLedgerEvent], limit: int = 100) -> str:
    summary = shadow_ledger_summary(events)
    text = f"Shadow Ledger (Events: {summary['count']})\n"
    for e in events[:limit]:
        text += f"[{e.created_at_utc}] {e.event_type.value} - {e.symbol or 'N/A'}\n"
    return text
