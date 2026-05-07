import pytest
from usa_signal_bot.paper.cash_ledger import (
    create_starting_cash_entry, create_cash_ledger_entry,
    ledger_entries_from_fill, calculate_cash_from_ledger
)
from usa_signal_bot.paper.virtual_account import create_virtual_account
from usa_signal_bot.core.enums import PaperCashLedgerEntryType, PaperOrderSide, PaperFillStatus
from usa_signal_bot.paper.paper_models import PaperFill, create_paper_fill_id

def test_starting_cash_entry():
    acct = create_virtual_account("test", 1000.0)
    entry = create_starting_cash_entry(acct)

    assert entry.account_id == acct.account_id
    assert entry.amount == 1000.0
    assert entry.entry_type == PaperCashLedgerEntryType.STARTING_CASH

def test_ledger_from_fill():
    acct = create_virtual_account("test", 1000.0)

    fill = PaperFill(
        fill_id=create_paper_fill_id(),
        order_id="mock",
        account_id=acct.account_id,
        symbol="AAPL",
        timeframe="1d",
        side=PaperOrderSide.BUY,
        quantity=10.0,
        fill_price=10.0,
        gross_notional=100.0,
        fees=1.0,
        slippage_cost=0.0,
        net_cash_impact=-101.0,
        status=PaperFillStatus.FILLED,
        filled_at_utc="2026-05-06T12:00:00Z"
    )

    entries = ledger_entries_from_fill(acct, fill, cash_after=899.0)
    assert len(entries) == 1
    assert entries[0].entry_type == PaperCashLedgerEntryType.BUY_DEBIT
    assert entries[0].amount == -101.0
    assert entries[0].cash_after == 899.0

def test_calculate_cash_from_ledger():
    acct = create_virtual_account("test", 1000.0)
    e1 = create_starting_cash_entry(acct)
    e2 = create_cash_ledger_entry(acct, PaperCashLedgerEntryType.BUY_DEBIT, -500.0, 500.0)
    e3 = create_cash_ledger_entry(acct, PaperCashLedgerEntryType.SELL_CREDIT, 200.0, 700.0)

    cash = calculate_cash_from_ledger([e1, e2, e3])
    assert cash == 700.0
