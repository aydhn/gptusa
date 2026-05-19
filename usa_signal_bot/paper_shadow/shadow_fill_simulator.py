from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowOrderIntent,
    ShadowFill,
    ShadowFillStatus,
    create_shadow_fill_id
)

def simulate_shadow_fill(intent: ShadowOrderIntent, default_price: float = 100.0, slippage_bps: float = 10.0, cost_bps: float = 5.0) -> ShadowFill:
    from usa_signal_bot.core.enums import ShadowOrderIntentStatus
    if intent.status in [ShadowOrderIntentStatus.BLOCKED, ShadowOrderIntentStatus.RISK_REJECTED, ShadowOrderIntentStatus.CANCELLED]:
        return reject_blocked_intent_fill(intent)

    price = intent.limit_price if intent.limit_price else default_price
    slippage = (price * slippage_bps) / 10000.0
    cost = (price * cost_bps) / 10000.0 * intent.quantity

    fill_price = price + slippage if intent.side.upper() == "BUY" else price - slippage

    return ShadowFill(
        fill_id=create_shadow_fill_id(intent.symbol),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        intent_id=intent.intent_id,
        symbol=intent.symbol,
        side=intent.side,
        requested_quantity=intent.quantity,
        filled_quantity=intent.quantity,
        simulated_cost_usd=cost,
        simulated_slippage_usd=slippage * intent.quantity,
        status=ShadowFillStatus.SIMULATED_FILLED,
        is_real_fill=False,
        warnings=[],
        errors=[],
        fill_price=fill_price
    )

def simulate_shadow_fills(intents: list[ShadowOrderIntent]) -> list[ShadowFill]:
    return [simulate_shadow_fill(i) for i in intents]

def reject_blocked_intent_fill(intent: ShadowOrderIntent) -> ShadowFill:
    return ShadowFill(
        fill_id=create_shadow_fill_id(intent.symbol),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        intent_id=intent.intent_id,
        symbol=intent.symbol,
        side=intent.side,
        requested_quantity=intent.quantity,
        filled_quantity=0.0,
        simulated_cost_usd=0.0,
        simulated_slippage_usd=0.0,
        status=ShadowFillStatus.BLOCKED,
        is_real_fill=False,
        warnings=[],
        errors=["Intent was blocked or rejected"]
    )

def validate_shadow_fills_safe(fills: list[ShadowFill]) -> list[str]:
    errors = []
    for fill in fills:
        if fill.is_real_fill:
            errors.append(f"Fill {fill.fill_id} is marked as real fill")
        for key, val in fill.metadata.items():
             if "broker" in str(key).lower() or "exchange" in str(key).lower():
                 errors.append(f"Fill {fill.fill_id} has broker-like metadata field: {key}")
    return errors

def shadow_fill_summary(fills: list[ShadowFill]) -> dict[str, Any]:
    return {
        "total": len(fills),
        "simulated_filled": sum(1 for f in fills if f.status == ShadowFillStatus.SIMULATED_FILLED),
        "blocked": sum(1 for f in fills if f.status == ShadowFillStatus.BLOCKED),
        "total_cost": sum(f.simulated_cost_usd for f in fills)
    }

def shadow_fills_to_text(fills: list[ShadowFill], limit: int = 50) -> str:
    summary = shadow_fill_summary(fills)
    text = f"Shadow Fills (Count: {summary['total']})\n"
    for fill in fills[:limit]:
        text += f"- {fill.symbol} {fill.side} {fill.filled_quantity} shares @ {fill.fill_price} (Status: {fill.status.value})\n"
    return text
