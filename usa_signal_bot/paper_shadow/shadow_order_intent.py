from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSignal, ShadowOrderIntent, create_shadow_order_intent_id, get_utc_now_str
)
from usa_signal_bot.core.enums import ShadowOrderIntentStatus

def build_shadow_order_intent_from_signal(signal: ShadowSignal, notional_usd: float = 1000.0, price: float | None = None) -> ShadowOrderIntent:
    return ShadowOrderIntent(
        intent_id=create_shadow_order_intent_id(signal.symbol),
        created_at_utc=get_utc_now_str(),
        symbol=signal.symbol,
        side=signal.side,
        quantity=notional_usd / price if price and price > 0 else 1.0,
        notional_usd=notional_usd,
        limit_price=price,
        source_signal_id=signal.signal_id,
        strategy_name=signal.strategy_name,
        status=ShadowOrderIntentStatus.DRAFT,
        is_real_order=False,
        broker_destination=None,
        warnings=[],
        errors=[]
    )

def build_shadow_order_intents(signals: List[ShadowSignal], default_notional_usd: float = 1000.0) -> List[ShadowOrderIntent]:
    return [build_shadow_order_intent_from_signal(s, default_notional_usd, 100.0) for s in signals]

def validate_shadow_order_intents_safe(intents: List[ShadowOrderIntent]) -> List[str]:
    errors = []
    for intent in intents:
        if intent.is_real_order:
            errors.append(f"Intent {intent.intent_id} is marked as real order.")
        if intent.broker_destination is not None:
            errors.append(f"Intent {intent.intent_id} has broker destination set.")
        if intent.quantity < 0 or intent.notional_usd < 0:
            errors.append(f"Intent {intent.intent_id} has negative quantity/notional.")
    return errors

def block_real_order_like_intents(intents: List[ShadowOrderIntent]) -> List[ShadowOrderIntent]:
    result = []
    for intent in intents:
        if intent.is_real_order or intent.broker_destination is not None:
            intent.status = ShadowOrderIntentStatus.BLOCKED
            intent.errors.append("Blocked due to real order-like properties.")
        result.append(intent)
    return result

def shadow_order_intent_summary(intents: List[ShadowOrderIntent]) -> Dict[str, Any]:
    return {
        "count": len(intents),
        "total_notional_usd": sum(i.notional_usd for i in intents)
    }

def shadow_order_intents_to_text(intents: List[ShadowOrderIntent], limit: int = 50) -> str:
    s = shadow_order_intent_summary(intents)
    return f"ShadowOrderIntents(count={s['count']}, notional={s['total_notional_usd']:.2f})"
