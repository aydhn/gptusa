from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSignal,
    ShadowOrderIntent,
    ShadowOrderIntentStatus,
    create_shadow_order_intent_id
)

def build_shadow_order_intent_from_signal(signal: ShadowSignal, notional_usd: float = 1000.0, price: float | None = None) -> ShadowOrderIntent:
    qty = notional_usd / price if price and price > 0 else 1.0
    return ShadowOrderIntent(
        intent_id=create_shadow_order_intent_id(signal.symbol),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=signal.symbol,
        side=signal.side,
        quantity=qty,
        notional_usd=notional_usd,
        status=ShadowOrderIntentStatus.DRAFT,
        is_real_order=False,
        warnings=[],
        errors=[],
        limit_price=price,
        source_signal_id=signal.signal_id,
        strategy_name=signal.strategy_name,
        broker_destination=None
    )

def build_shadow_order_intents(signals: list[ShadowSignal], default_notional_usd: float = 1000.0) -> list[ShadowOrderIntent]:
    return [build_shadow_order_intent_from_signal(s, default_notional_usd, 100.0) for s in signals]

def validate_shadow_order_intents_safe(intents: list[ShadowOrderIntent]) -> list[str]:
    errors = []
    for intent in intents:
        if intent.is_real_order:
            errors.append(f"Intent {intent.intent_id} is marked as real order")
        if intent.broker_destination is not None:
            errors.append(f"Intent {intent.intent_id} has a broker destination")
        for key, val in intent.metadata.items():
            if "broker" in str(key).lower() or "sent" in str(key).lower():
                errors.append(f"Intent {intent.intent_id} has broker-like metadata field: {key}")
    return errors

def block_real_order_like_intents(intents: list[ShadowOrderIntent]) -> list[ShadowOrderIntent]:
    safe_intents = []
    for intent in intents:
        if validate_shadow_order_intents_safe([intent]):
            intent.status = ShadowOrderIntentStatus.BLOCKED
            intent.errors.append("Blocked due to unsafe attributes")
        safe_intents.append(intent)
    return safe_intents

def shadow_order_intent_summary(intents: list[ShadowOrderIntent]) -> dict[str, Any]:
    return {
        "count": len(intents),
        "status_counts": {status.name: sum(1 for i in intents if i.status == status) for status in ShadowOrderIntentStatus}
    }

def shadow_order_intents_to_text(intents: list[ShadowOrderIntent], limit: int = 50) -> str:
    summary = shadow_order_intent_summary(intents)
    text = f"Shadow Order Intents (Count: {summary['count']})\n"
    for intent in intents[:limit]:
        text += f"- {intent.symbol} {intent.side} {intent.quantity} shares (Status: {intent.status.value})\n"
    return text
