from typing import Any, Dict
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowPortfolioState, ShadowSignal,
    ShadowOrderIntent, ShadowFill, ShadowLedgerEvent, ShadowPnLSnapshot,
    ShadowRehearsalSession, ShadowRehearsalReview
)

def shadow_context_to_text(item: ShadowSimulationContext) -> str:
    return f"ShadowContext({item.context_id})"

def shadow_portfolio_to_text(item: ShadowPortfolioState) -> str:
    return f"ShadowPortfolio({item.portfolio_id}, eq={item.equity_usd})"

def shadow_signal_to_text(item: ShadowSignal) -> str:
    return f"ShadowSignal({item.symbol}, side={item.side})"

def shadow_order_intent_to_text(item: ShadowOrderIntent) -> str:
    return f"ShadowIntent({item.symbol}, side={item.side}, qty={item.quantity})"

def shadow_fill_to_text(item: ShadowFill) -> str:
    return f"ShadowFill({item.symbol}, filled={item.filled_quantity}, status={item.status.value})"

def shadow_ledger_event_to_text(item: ShadowLedgerEvent) -> str:
    return f"ShadowLedgerEvent({item.event_type.value})"

def shadow_pnl_snapshot_to_text(item: ShadowPnLSnapshot) -> str:
    return f"ShadowPnL({item.total_pnl_usd:.2f})"

def shadow_rehearsal_session_to_text(item: ShadowRehearsalSession, limit: int = 100) -> str:
    return f"ShadowSession({item.session_id}, status={item.status.value})"

def shadow_rehearsal_review_to_text(item: ShadowRehearsalReview, limit: int = 100) -> str:
    return f"ShadowReview({item.review_id}, sessions={len(item.sessions)})"

def shadow_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"ShadowStoreSummary({summary})"

def paper_shadow_limitations_text() -> str:
    return (
        "PAPER SHADOW LIMITATIONS:\n"
        "- This is a simulated environment only.\n"
        "- NO real orders are sent to any broker.\n"
        "- NO actual paper trading state is mutated.\n"
        "- Fills are purely simulated.\n"
        "- Order intents are NOT broker orders.\n"
        "- NO Telegram notifications are actually sent in real mode.\n"
        "- A successful shadow rehearsal is NOT an approval for live trading.\n"
        "- Results DO NOT constitute investment advice."
    )
