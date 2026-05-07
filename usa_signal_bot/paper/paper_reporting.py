from typing import List, Optional
from pathlib import Path

from usa_signal_bot.paper.paper_models import (
    VirtualAccount, PaperOrderIntent, PaperOrder, PaperFill, PaperPosition,
    CashLedgerEntry, PaperEquitySnapshot, PaperTrade, PaperEngineRunResult
)
from usa_signal_bot.paper.paper_engine import PaperEngineConfig
from usa_signal_bot.paper.paper_validation import PaperValidationReport
from usa_signal_bot.paper.virtual_account import virtual_account_to_text
from usa_signal_bot.paper.order_lifecycle import order_lifecycle_to_text
from usa_signal_bot.paper.paper_fills import paper_fill_to_text
from usa_signal_bot.paper.paper_positions import paper_positions_to_text
from usa_signal_bot.paper.cash_ledger import cash_ledger_to_text
from usa_signal_bot.paper.equity_snapshots import paper_equity_snapshots_to_text
from usa_signal_bot.paper.paper_journal import paper_trades_to_text, paper_trade_summary

def paper_engine_config_to_text(config: PaperEngineConfig) -> str:
    lines = [
        "--- PAPER ENGINE CONFIG ---",
        f"Execution Mode: {config.execution_mode.value if hasattr(config.execution_mode, 'value') else config.execution_mode}",
        f"Starting Cash: ${config.starting_cash:,.2f}",
        f"Fee Bps: {config.fee_bps} | Slippage Bps: {config.slippage_bps}",
        f"Max Positions: {config.max_positions} | Max Order Notional: ${config.max_order_notional:,.2f}",
        f"Allow Short: {config.allow_short}"
    ]
    return "\n".join(lines)

def virtual_account_report_to_text(account: VirtualAccount) -> str:
    return virtual_account_to_text(account)

def paper_order_intent_to_text(intent: PaperOrderIntent) -> str:
    side = intent.side.value if hasattr(intent.side, 'value') else intent.side
    otype = intent.order_type.value if hasattr(intent.order_type, 'value') else intent.order_type
    qty = f"Qty: {intent.quantity}"
    limit = f" | Limit: ${intent.limit_price}" if intent.limit_price else ""
    return f"INTENT: {side} {intent.symbol} ({intent.timeframe}) | {otype} | {qty}{limit}"

def paper_order_to_text(order: PaperOrder) -> str:
    intent_txt = paper_order_intent_to_text(order.intent)
    status = order.status.value if hasattr(order.status, 'value') else order.status
    rej = f" | Reject: {order.reject_reason}" if order.reject_reason else ""
    return f"ORDER {order.order_id}: [{status}]{rej}\n  {intent_txt}"

def paper_positions_report_to_text(positions: List[PaperPosition], limit: int = 30) -> str:
    return paper_positions_to_text(positions, limit)

def cash_ledger_report_to_text(entries: List[CashLedgerEntry], limit: int = 30) -> str:
    return cash_ledger_to_text(entries, limit)

def paper_equity_snapshot_report_to_text(snapshot: PaperEquitySnapshot) -> str:
    return paper_equity_snapshots_to_text([snapshot])

def paper_trades_report_to_text(trades: List[PaperTrade], limit: int = 30) -> str:
    lines = [paper_trades_to_text(trades, limit)]
    if trades:
        summary = paper_trade_summary(trades)
        lines.append("\n--- TRADE SUMMARY ---")
        lines.append(f"Total: {summary['total_trades']} | Closed: {summary['closed_trades']} | Open: {summary['open_trades']}")
        if summary['closed_trades'] > 0:
            lines.append(f"Win Rate: {summary['win_rate']*100:.1f}% ({summary['winning_trades']}W / {summary['losing_trades']}L)")
            lines.append(f"Total Net PnL: ${summary['total_net_pnl']:,.2f} | Total Fees: ${summary['total_fees']:,.2f}")
            lines.append(f"Avg Win: ${summary['avg_win']:,.2f} | Avg Loss: ${summary['avg_loss']:,.2f}")
    return "\n".join(lines)

def paper_limitations_text() -> str:
    return (
        "*** DISCLAIMER: LOCAL PAPER TRADING ONLY ***\n"
        "1. This is a local simulation. NO BROKER ORDERS or live executions were created.\n"
        "2. Fills are simulated using historical local cache and simplistic assumptions.\n"
        "3. Slippage and fees are hypothetical and may not reflect real market conditions.\n"
        "4. This system does not account for market impact, liquidity constraints, or latency.\n"
        "5. The results are strictly for research and DO NOT constitute investment advice.\n"
        "********************************************"
    )

def paper_engine_run_result_to_text(result: PaperEngineRunResult, limit: int = 30) -> str:
    lines = [
        "===============================================",
        f"PAPER ENGINE RUN: {result.run_id}",
        f"Status: {result.status.value if hasattr(result.status, 'value') else result.status}",
        f"Time: {result.created_at_utc}",
        "===============================================\n",
        virtual_account_report_to_text(result.account),
        ""
    ]

    if result.orders:
        lines.append("--- ORDERS ---")
        for o in result.orders[:limit]:
            lines.append(paper_order_to_text(o))
        if len(result.orders) > limit:
            lines.append(f"... {len(result.orders) - limit} more orders")
        lines.append("")

    if result.positions:
        lines.append(paper_positions_report_to_text(result.positions, limit))
        lines.append("")

    if result.trades:
        lines.append(paper_trades_report_to_text(result.trades, limit))
        lines.append("")

    if result.equity_snapshots:
        lines.append(paper_equity_snapshot_report_to_text(result.equity_snapshots[-1]))
        lines.append("")

    if result.errors:
        lines.append("--- ERRORS ---")
        for e in result.errors:
            lines.append(f"  ! {e}")
        lines.append("")

    if result.warnings:
        lines.append("--- WARNINGS ---")
        for w in result.warnings:
            lines.append(f"  * {w}")
        lines.append("")

    lines.append(paper_limitations_text())

    return "\n".join(lines)

def write_paper_report_json(path: Path, result: PaperEngineRunResult, validation_report: Optional[PaperValidationReport] = None) -> Path:
    from usa_signal_bot.paper.paper_store import _atomic_write_json, paper_engine_run_result_to_dict
    from dataclasses import asdict

    data = {
        "run": paper_engine_run_result_to_dict(result),
        "validation": asdict(validation_report) if validation_report else None,
        "disclaimer": "LOCAL PAPER TRADING ONLY. NO BROKER INTEGRATION. NOT INVESTMENT ADVICE."
    }

    return _atomic_write_json(path, data)
