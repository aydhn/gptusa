import pytest
from usa_signal_bot.core.enums import BacktestOrderSide, BacktestFillStatus, BacktestPositionSide
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.backtesting.position_models import (
    create_flat_position, update_position_with_fill, mark_position_to_market, position_to_dict
)

def test_create_flat_position():
    pos = create_flat_position("AAPL")
    assert pos.side == BacktestPositionSide.FLAT
    assert pos.quantity == 0

def test_buy_fill_opens_long():
    pos = create_flat_position("AAPL")
    fill = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)
    res = update_position_with_fill(pos, fill)
    assert res.position.side == BacktestPositionSide.LONG
    assert res.position.quantity == 10
    assert res.position.average_price == 100.0
    assert res.cash_delta == -1000.0

def test_sell_fill_closes_long():
    pos = create_flat_position("AAPL")
    fill1 = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)
    res1 = update_position_with_fill(pos, fill1)

    fill2 = BacktestFill("f2", "o2", "s2", "AAPL", "1d", "2023", BacktestOrderSide.SELL, 10, 110.0, BacktestFillStatus.FILLED)
    res2 = update_position_with_fill(res1.position, fill2)

    assert res2.position.side == BacktestPositionSide.FLAT
    assert res2.position.quantity == 0
    assert res2.realized_pnl_delta == 100.0
    assert res2.cash_delta == 1100.0

def test_mark_to_market():
    pos = create_flat_position("AAPL")
    fill = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)
    res = update_position_with_fill(pos, fill)

    marked = mark_position_to_market(res.position, 110.0, "2023")
    assert marked.unrealized_pnl == 100.0

def test_oversell():
    pos = create_flat_position("AAPL")
    fill1 = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)
    res1 = update_position_with_fill(pos, fill1)

    fill2 = BacktestFill("f2", "o2", "s2", "AAPL", "1d", "2023", BacktestOrderSide.SELL, 15, 110.0, BacktestFillStatus.FILLED)
    res2 = update_position_with_fill(res1.position, fill2)

    assert res2.position.side == BacktestPositionSide.FLAT
    assert res2.position.quantity == 0
    assert "WARNING" in res2.message

def test_position_to_dict():
    pos = create_flat_position("AAPL")
    d = position_to_dict(pos)
    assert d["symbol"] == "AAPL"
