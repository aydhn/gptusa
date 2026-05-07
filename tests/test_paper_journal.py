import pytest
from usa_signal_bot.paper.paper_journal import (
    build_paper_trades_from_fills, pair_paper_buy_sell_fills,
    paper_trade_summary
)
from usa_signal_bot.paper.paper_models import PaperFill, create_paper_fill_id
from usa_signal_bot.core.enums import PaperOrderSide, PaperTradeStatus, PaperFillStatus

def _mock_fill(side, qty, price, fees=0.0):
    return PaperFill(
        fill_id=create_paper_fill_id(),
        order_id="mock",
        account_id="acct",
        symbol="AAPL",
        timeframe="1d",
        side=side,
        quantity=qty,
        fill_price=price,
        gross_notional=qty*price,
        fees=fees,
        slippage_cost=0.0,
        net_cash_impact=0.0,
        status=PaperFillStatus.FILLED,
        filled_at_utc="2026-05-06T12:00:00Z"
    )

def test_pair_buy_sell_fills_full():
    f1 = _mock_fill(PaperOrderSide.BUY, 10.0, 100.0, 1.0)
    f2 = _mock_fill(PaperOrderSide.SELL, 10.0, 110.0, 1.0)

    closed, open_t, warns = pair_paper_buy_sell_fills([f1, f2])

    assert len(closed) == 1
    assert len(open_t) == 0
    assert not warns

    t = closed[0]
    assert t.status == PaperTradeStatus.CLOSED
    assert t.quantity == 10.0
    assert t.entry_price == 100.0
    assert t.exit_price == 110.0
    assert t.gross_pnl == 100.0 # 10 * (110 - 100)
    assert t.total_fees == 2.0
    assert t.net_pnl == 98.0

def test_pair_buy_sell_fills_partial():
    f1 = _mock_fill(PaperOrderSide.BUY, 20.0, 100.0, 2.0)
    f2 = _mock_fill(PaperOrderSide.SELL, 10.0, 150.0, 1.5)

    closed, open_t, warns = pair_paper_buy_sell_fills([f1, f2])

    assert len(closed) == 1
    assert len(open_t) == 1

    c = closed[0]
    assert c.quantity == 10.0
    assert c.gross_pnl == 500.0 # 10 * 50
    assert c.total_fees == 2.5 # half of buy fee (1.0) + all of sell fee (1.5)
    assert c.net_pnl == 497.5

    o = open_t[0]
    assert o.quantity == 10.0
    assert o.status == PaperTradeStatus.OPEN
    assert o.total_fees == 1.0 # remaining half of buy fee

def test_paper_trade_summary():
    f1 = _mock_fill(PaperOrderSide.BUY, 10.0, 100.0)
    f2 = _mock_fill(PaperOrderSide.SELL, 10.0, 110.0) # Win

    f3 = _mock_fill(PaperOrderSide.BUY, 10.0, 100.0)
    f4 = _mock_fill(PaperOrderSide.SELL, 10.0, 90.0) # Loss

    f5 = _mock_fill(PaperOrderSide.BUY, 10.0, 100.0) # Open

    trades = build_paper_trades_from_fills([f1, f2, f3, f4, f5])

    summary = paper_trade_summary(trades)
    assert summary["total_trades"] == 3
    assert summary["closed_trades"] == 2
    assert summary["open_trades"] == 1
    assert summary["winning_trades"] == 1
    assert summary["losing_trades"] == 1
    assert summary["win_rate"] == 0.5
    assert summary["total_net_pnl"] == 0.0 # 100 win + (-100 loss) = 0
