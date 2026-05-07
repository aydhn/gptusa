from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pathlib import Path
import json

from usa_signal_bot.core.enums import PaperCashLedgerEntryType, PaperOrderSide
from usa_signal_bot.paper.paper_models import VirtualAccount, CashLedgerEntry, PaperFill, create_cash_ledger_entry_id

def create_starting_cash_entry(account: VirtualAccount) -> CashLedgerEntry:
    return CashLedgerEntry(
        entry_id=create_cash_ledger_entry_id("cash_start"),
        account_id=account.account_id,
        timestamp_utc=account.created_at_utc,
        entry_type=PaperCashLedgerEntryType.STARTING_CASH,
        amount=account.starting_cash,
        cash_after=account.starting_cash,
        description="Starting cash"
    )

def create_cash_ledger_entry(
    account: VirtualAccount,
    entry_type: PaperCashLedgerEntryType,
    amount: float,
    cash_after: float,
    related_order_id: Optional[str] = None,
    related_fill_id: Optional[str] = None,
    description: Optional[str] = None
) -> CashLedgerEntry:
    return CashLedgerEntry(
        entry_id=create_cash_ledger_entry_id(),
        account_id=account.account_id,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        entry_type=entry_type,
        amount=amount,
        cash_after=cash_after,
        related_order_id=related_order_id,
        related_fill_id=related_fill_id,
        description=description
    )

def ledger_entries_from_fill(account: VirtualAccount, fill: PaperFill, cash_after: float) -> List[CashLedgerEntry]:
    entries = []

    if fill.side == PaperOrderSide.BUY:
        entry_type = PaperCashLedgerEntryType.BUY_DEBIT
        desc = f"Buy {fill.quantity} {fill.symbol} @ ${fill.fill_price:.2f} (Fee: ${fill.fees:.2f})"
    elif fill.side == PaperOrderSide.SELL:
        entry_type = PaperCashLedgerEntryType.SELL_CREDIT
        desc = f"Sell {fill.quantity} {fill.symbol} @ ${fill.fill_price:.2f} (Fee: ${fill.fees:.2f})"
    else:
        return []

    entry = create_cash_ledger_entry(
        account=account,
        entry_type=entry_type,
        amount=fill.net_cash_impact,
        cash_after=cash_after,
        related_order_id=fill.order_id,
        related_fill_id=fill.fill_id,
        description=desc
    )

    entry.timestamp_utc = fill.filled_at_utc
    entries.append(entry)

    return entries

def calculate_cash_from_ledger(entries: List[CashLedgerEntry]) -> float:
    if not entries:
        return 0.0

    cash = 0.0
    for entry in entries:
        if entry.entry_type == PaperCashLedgerEntryType.STARTING_CASH:
            cash = entry.amount
        else:
            cash += entry.amount

    return cash

def cash_ledger_to_text(entries: List[CashLedgerEntry], limit: int = 30) -> str:
    lines = ["--- CASH LEDGER ---"]

    if not entries:
        lines.append("No entries.")
        return "\n".join(lines)

    sorted_entries = sorted(entries, key=lambda x: x.timestamp_utc, reverse=True)

    for e in sorted_entries[:limit]:
        etype = e.entry_type.value if hasattr(e.entry_type, 'value') else e.entry_type
        desc = f" | {e.description}" if e.description else ""
        sign = "+" if e.amount >= 0 else ""
        lines.append(f"{e.timestamp_utc} | {etype} | Amount: {sign}${e.amount:,.2f} | Bal: ${e.cash_after:,.2f}{desc}")

    if len(sorted_entries) > limit:
        lines.append(f"... and {len(sorted_entries) - limit} more")

    return "\n".join(lines)

def write_cash_ledger_jsonl(path: Path, entries: List[CashLedgerEntry]) -> Path:
    from usa_signal_bot.paper.paper_models import cash_ledger_entry_to_dict
    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(cash_ledger_entry_to_dict(entry)) + "\n")
    return path

def read_cash_ledger_jsonl(path: Path) -> List[Dict[str, Any]]:
    res = []
    if not path.exists():
        return res
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    res.append(json.loads(line))
                except Exception:
                    pass
    return res
