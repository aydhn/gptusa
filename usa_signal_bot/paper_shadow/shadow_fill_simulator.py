from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowOrderIntent, ShadowFill, create_shadow_fill_id, get_utc_now_str
)
from usa_signal_bot.core.enums import ShadowFillStatus, ShadowOrderIntentStatus

def simulate_shadow_fill(intent: ShadowOrderIntent, default_price: float = 100.0, slippage_bps: float = 10.0, cost_bps: float = 5.0) -> ShadowFill:
    if intent.status != ShadowOrderIntentStatus.RISK_APPROVED:
        return reject_blocked_intent_fill(intent)

    price = intent.limit_price or default_price
    notional = intent.quantity * price
    cost = notional * (cost_bps / 10000.0)
    slippage = notional * (slippage_bps / 10000.0)

    return ShadowFill(
        fill_id=create_shadow_fill_id(intent.symbol),
        created_at_utc=get_utc_now_str(),
        intent_id=intent.intent_id,
        symbol=intent.symbol,
        side=intent.side,
        requested_quantity=intent.quantity,
        filled_quantity=intent.quantity,
        fill_price=price,
        simulated_cost_usd=cost,
        simulated_slippage_usd=slippage,
        status=ShadowFillStatus.SIMULATED_FILLED,
        is_real_fill=False,
        warnings=[],
        errors=[]
    )

def simulate_shadow_fills(intents: List[ShadowOrderIntent]) -> List[ShadowFill]:
    return [simulate_shadow_fill(intent) for intent in intents]

def reject_blocked_intent_fill(intent: ShadowOrderIntent) -> ShadowFill:
    return ShadowFill(
        fill_id=create_shadow_fill_id(intent.symbol),
        created_at_utc=get_utc_now_str(),
        intent_id=intent.intent_id,
        symbol=intent.symbol,
        side=intent.side,
        requested_quantity=intent.quantity,
        filled_quantity=0.0,
        fill_price=None,
        simulated_cost_usd=0.0,
        simulated_slippage_usd=0.0,
        status=ShadowFillStatus.BLOCKED if intent.status == ShadowOrderIntentStatus.BLOCKED else ShadowFillStatus.SIMULATED_REJECTED,
        is_real_fill=False,
        warnings=[],
        errors=["Intent was not approved."]
    )

def validate_shadow_fills_safe(fills: List[ShadowFill]) -> List[str]:
    errors = []
    for fill in fills:
        if fill.is_real_fill:
            errors.append(f"Fill {fill.fill_id} is marked as real fill.")
        if fill.simulated_cost_usd < 0 or fill.simulated_slippage_usd < 0:
            errors.append(f"Fill {fill.fill_id} has negative cost/slippage.")
    return errors

def shadow_fill_summary(fills: List[ShadowFill]) -> Dict[str, Any]:
    return {
        "count": len(fills),
        "filled": sum(1 for f in fills if f.status == ShadowFillStatus.SIMULATED_FILLED),
        "total_cost_usd": sum(f.simulated_cost_usd for f in fills)
    }

def shadow_fills_to_text(fills: List[ShadowFill], limit: int = 50) -> str:
    s = shadow_fill_summary(fills)
    return f"ShadowFills(count={s['count']}, filled={s['filled']}, cost={s['total_cost_usd']:.2f})"
