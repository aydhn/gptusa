from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext,
    ShadowPortfolioState,
    ShadowSignal,
    ShadowOrderIntent,
    ShadowFill,
    ShadowLedgerEvent,
    ShadowPnLSnapshot,
    ShadowRehearsalSession,
    ShadowRehearsalReview
)
from usa_signal_bot.paper_shadow.simulation_context import shadow_context_to_text
from usa_signal_bot.paper_shadow.shadow_portfolio import shadow_portfolio_to_text
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import shadow_signals_to_text
from usa_signal_bot.paper_shadow.shadow_order_intent import shadow_order_intents_to_text
from usa_signal_bot.paper_shadow.shadow_fill_simulator import shadow_fills_to_text
from usa_signal_bot.paper_shadow.shadow_ledger import shadow_ledger_to_text
from usa_signal_bot.paper_shadow.shadow_pnl_tracker import shadow_pnl_to_text

def shadow_signal_to_text(item: ShadowSignal) -> str:
    return f"Shadow Signal: {item.symbol} {item.side} (Score: {item.score})"

def shadow_order_intent_to_text(item: ShadowOrderIntent) -> str:
    return f"Shadow Intent: {item.symbol} {item.side} {item.quantity} (Status: {item.status.value})"

def shadow_fill_to_text(item: ShadowFill) -> str:
    return f"Shadow Fill: {item.symbol} {item.side} {item.filled_quantity} (Status: {item.status.value})"

def shadow_ledger_event_to_text(item: ShadowLedgerEvent) -> str:
    return f"Ledger Event: {item.event_type.value} [{item.created_at_utc}]"

def shadow_pnl_snapshot_to_text(item: ShadowPnLSnapshot) -> str:
    return f"PnL Snapshot: Equity ${item.equity_usd:.2f} (Total PnL: ${item.total_pnl_usd:.2f})"

def shadow_rehearsal_session_to_text(item: ShadowRehearsalSession, limit: int = 100) -> str:
    text = f"Shadow Rehearsal Session: {item.session_id}\n"
    text += f"Status: {item.status.value}\n"
    if item.context:
        text += f"\n{shadow_context_to_text(item.context)}\n"
    if item.portfolio_state:
        text += f"\n{shadow_portfolio_to_text(item.portfolio_state)}\n"
    text += f"\n{shadow_signals_to_text(item.signals, limit)}\n"
    text += f"\n{shadow_order_intents_to_text(item.order_intents, limit)}\n"
    text += f"\n{shadow_fills_to_text(item.fills, limit)}\n"
    text += f"\n{shadow_ledger_to_text(item.ledger_events, limit)}\n"
    text += f"\n{shadow_pnl_to_text(item.pnl_snapshots, limit)}\n"
    text += f"\n{paper_shadow_limitations_text()}\n"
    return text

def shadow_rehearsal_review_to_text(item: ShadowRehearsalReview, limit: int = 100) -> str:
    text = f"Shadow Rehearsal Review: {item.review_id}\n"
    text += f"Type: {item.report_type.value}\n"
    text += f"Sessions: {len(item.sessions)}\n"
    for s in item.sessions[:limit]:
         text += f"\n---\n{shadow_rehearsal_session_to_text(s, limit)}\n"
    return text

def shadow_store_summary_to_text(summary: dict[str, Any]) -> str:
    text = "Shadow Store Summary\n"
    for k, v in summary.items():
        text += f"{k}: {v}\n"
    return text

def paper_shadow_limitations_text() -> str:
    return """
*** PAPER-SHADOW LIMITATIONS & DISCLAIMERS ***
1. This is an isolated shadow simulation. No broker orders were generated or sent.
2. The portfolio and fills are simulated and do NOT modify the actual local paper state.
3. Performance and PnL numbers are simulated and do NOT constitute investment advice.
4. A 'PASS' status in this shadow rehearsal is NOT an approval for live trading.
5. No real telegram messages were sent during this simulation.
"""
