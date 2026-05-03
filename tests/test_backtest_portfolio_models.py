import pytest
from usa_signal_bot.core.enums import BacktestOrderSide, BacktestFillStatus, BacktestPositionSide
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.backtesting.portfolio_models import (
    create_portfolio, apply_fill_to_portfolio, create_portfolio_snapshot, validate_portfolio
)

def test_create_portfolio():
    port = create_portfolio(10000.0)
    assert port.cash == 10000.0
    assert port.starting_cash == 10000.0

def test_apply_buy_sell():
    port = create_portfolio(10000.0)
    fill_buy = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)

    port = apply_fill_to_portfolio(port, fill_buy, 100.0)
    assert port.cash == 9000.0
    assert "AAPL" in port.positions
    assert port.positions["AAPL"].side == BacktestPositionSide.LONG

    fill_sell = BacktestFill("f2", "o2", "s2", "AAPL", "1d", "2023", BacktestOrderSide.SELL, 10, 110.0, BacktestFillStatus.FILLED)
    port = apply_fill_to_portfolio(port, fill_sell, 110.0)
    assert port.cash == 10100.0
    assert port.realized_pnl == 100.0

def test_insufficient_cash():
    port = create_portfolio(100.0)
    fill_buy = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)

    port = apply_fill_to_portfolio(port, fill_buy, 100.0)
    assert port.cash == 100.0
    assert "AAPL" in port.positions
    assert port.positions["AAPL"].side == BacktestPositionSide.FLAT
    assert len(port.warnings) > 0

def test_create_snapshot():
    port = create_portfolio(10000.0)
    fill_buy = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)
    port = apply_fill_to_portfolio(port, fill_buy, 100.0)

    snap = create_portfolio_snapshot(port, {"AAPL": 110.0}, "2023")
    assert snap.equity == 10100.0

def test_validate_portfolio():
    port = create_portfolio(10000.0)
    validate_portfolio(port)
