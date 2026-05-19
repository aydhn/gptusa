from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowPortfolioState,
    ShadowSimulationContext,
    ShadowOrderIntent
)

def build_shadow_rebalance_preview(portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> dict[str, Any]:
    intents = shadow_rebalance_intents_from_portfolio(portfolio)
    return {
        "portfolio_id": portfolio.portfolio_id,
        "intents": [i.intent_id for i in intents],
        "is_safe": not validate_shadow_rebalance_safe({"intents": intents})
    }

def shadow_rebalance_intents_from_portfolio(portfolio: ShadowPortfolioState) -> list[ShadowOrderIntent]:
    # Dummy logic to generate balancing intents
    from usa_signal_bot.paper_shadow.shadow_models import ShadowOrderIntent, ShadowOrderIntentStatus, create_shadow_order_intent_id
    from datetime import datetime, timezone
    intents = []
    for pos in portfolio.positions:
        if pos.quantity > 0:
             intents.append(ShadowOrderIntent(
                intent_id=create_shadow_order_intent_id(pos.symbol),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                symbol=pos.symbol,
                side="SELL",
                quantity=pos.quantity * 0.1, # Dummy rebalance rule
                notional_usd=pos.market_value_usd * 0.1,
                status=ShadowOrderIntentStatus.DRAFT,
                is_real_order=False,
                warnings=[],
                errors=[]
             ))
    return intents

def validate_shadow_rebalance_safe(payload: dict[str, Any]) -> list[str]:
    from usa_signal_bot.paper_shadow.shadow_order_intent import validate_shadow_order_intents_safe
    errors = []
    intents = payload.get("intents", [])
    if intents:
        errors.extend(validate_shadow_order_intents_safe(intents))
    return errors

def shadow_rebalance_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "intent_count": len(payload.get("intents", [])),
        "is_safe": payload.get("is_safe", False)
    }

def shadow_rebalance_to_text(payload: dict[str, Any]) -> str:
    summary = shadow_rebalance_summary(payload)
    text = f"Shadow Rebalance Preview\n"
    text += f"Intents Generated: {summary['intent_count']}\n"
    text += f"Safe: {summary['is_safe']}\n"
    text += "Note: No broker orders generated. No paper state mutated."
    return text
