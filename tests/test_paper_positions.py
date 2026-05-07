import pytest
from usa_signal_bot.paper.paper_positions import (
    create_flat_paper_position, update_paper_position_with_fill,
    mark_paper_position_to_market, calculate_paper_unrealized_pnl
)
from usa_signal_bot.paper.paper_models import PaperFill, create_paper_fill_id
from usa_signal_bot.core.enums import PaperPositionSide, PaperOrderSide, PaperFillStatus

def _mock_fill(side, qty, price):
    return PaperFill(
        fill_id=create_paper_fill_id(),
        order_id="mock_order",
        account_id="mock_acct",
        symbol="AAPL",
        timeframe="1d",
        side=side,
        quantity=qty,
        fill_price=price,
        gross_notional=qty * price,
        fees=0.0,
        slippage_cost=0.0,
        net_cash_impact=0.0,
        status=PaperFillStatus.FILLED,
        filled_at_utc="2026-05-06T12:00:00Z"
    )

def test_flat_position():
    pos = create_flat_paper_position("AAPL")
    assert pos.symbol == "AAPL"
    assert pos.quantity == 0.0
    assert pos.side == PaperPositionSide.FLAT

def test_update_position_buy():
    pos = create_flat_paper_position("AAPL")
    fill1 = _mock_fill(PaperOrderSide.BUY, 10.0, 100.0)
    pos = update_paper_position_with_fill(pos, fill1)

    assert pos.side == PaperPositionSide.LONG
    assert pos.quantity == 10.0
    assert pos.average_price == 100.0

    # Second buy updates average price
    fill2 = _mock_fill(PaperOrderSide.BUY, 10.0, 150.0)
    pos = update_paper_position_with_fill(pos, fill2)

    assert pos.quantity == 20.0
    assert pos.average_price == 125.0

def test_update_position_sell():
    pos = create_flat_paper_position("AAPL")
    pos = update_paper_position_with_fill(pos, _mock_fill(PaperOrderSide.BUY, 20.0, 100.0))

    # Partial sell
    pos = update_paper_position_with_fill(pos, _mock_fill(PaperOrderSide.SELL, 10.0, 150.0))

    assert pos.quantity == 10.0
    assert pos.average_price == 100.0 # Average price doesn't change on sell
    assert pos.realized_pnl == 500.0 # (150 - 100) * 10

    # Full close
    pos = update_paper_position_with_fill(pos, _mock_fill(PaperOrderSide.SELL, 10.0, 200.0))

    assert pos.quantity == 0.0
    assert pos.side == PaperPositionSide.FLAT
    assert pos.realized_pnl == 1500.0 # 500 + ((200 - 100) * 10)

def test_mark_to_market():
    pos = create_flat_paper_position("AAPL")
    pos = update_paper_position_with_fill(pos, _mock_fill(PaperOrderSide.BUY, 10.0, 100.0))

    pos = mark_paper_position_to_market(pos, 150.0)
    assert pos.market_price == 150.0
    assert pos.market_value == 1500.0
    assert pos.unrealized_pnl == 500.0
