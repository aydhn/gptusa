from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import ShadowPortfolioState, ShadowSimulationContext, ShadowOrderIntent
from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intents

def build_shadow_rebalance_preview(portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> Dict[str, Any]:
    return {
        "status": "preview_only",
        "intents": [],
        "warnings": ["Shadow rebalance preview does not create real orders."]
    }

def shadow_rebalance_intents_from_portfolio(portfolio: ShadowPortfolioState) -> List[ShadowOrderIntent]:
    return []

def validate_shadow_rebalance_safe(payload: Dict[str, Any]) -> List[str]:
    return []

def shadow_rebalance_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload

def shadow_rebalance_to_text(payload: Dict[str, Any]) -> str:
    return "ShadowRebalancePreview(safe=True)"
