import pytest
from usa_signal_bot.paper.equity_snapshots import (
    create_paper_equity_snapshot, calculate_paper_gross_exposure,
    calculate_paper_net_exposure, calculate_paper_unrealized_pnl_total
)
from usa_signal_bot.paper.virtual_account import create_virtual_account
from usa_signal_bot.paper.paper_positions import create_flat_paper_position, update_paper_position_with_fill
from usa_signal_bot.paper.paper_models import PaperFill, create_paper_fill_id
from usa_signal_bot.core.enums import PaperOrderSide, PaperFillStatus

def _mock_fill(acct, sym, side, qty, price):
    return PaperFill(
        fill_id=create_paper_fill_id(),
        order_id="mock",
        account_id=acct.account_id,
        symbol=sym,
        timeframe="1d",
        side=side,
        quantity=qty,
        fill_price=price,
        gross_notional=qty*price,
        fees=0.0,
        slippage_cost=0.0,
        net_cash_impact=0.0,
        status=PaperFillStatus.FILLED,
        filled_at_utc="2026-05-06T12:00:00Z"
    )

def test_equity_snapshot_calculations():
    acct = create_virtual_account("test", 1000.0)
    acct.cash = 500.0 # Pretend we spent 500

    pos1 = create_flat_paper_position("AAPL")
    pos1 = update_paper_position_with_fill(pos1, _mock_fill(acct, "AAPL", PaperOrderSide.BUY, 10.0, 50.0))

    prices = {"AAPL": 60.0} # Price went up

    # Gross exposure = 10 * 60 = 600
    assert calculate_paper_gross_exposure([pos1], prices) == 600.0

    # Net exposure = 600 (long only)
    assert calculate_paper_net_exposure([pos1], prices) == 600.0

    # Unrealized PnL = (60 - 50) * 10 = 100
    assert calculate_paper_unrealized_pnl_total([pos1], prices) == 100.0

    snap = create_paper_equity_snapshot(acct, [pos1], prices, "2026-05-06T12:00:00Z")

    assert snap.cash == 500.0
    assert snap.equity == 1100.0 # 500 cash + 600 market value
    assert snap.gross_exposure == 600.0
    assert snap.unrealized_pnl == 100.0
    assert snap.open_positions == 1
