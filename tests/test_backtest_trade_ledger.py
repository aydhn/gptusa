import pytest
from usa_signal_bot.backtesting.trade_ledger import (
    TradeLedger, BacktestTrade, create_trade_id, pair_long_fills_into_trades,
    build_trade_ledger_from_fills, ledger_to_text, validate_trade_ledger
)
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.core.enums import BacktestOrderSide, BacktestFillStatus

@pytest.fixture
def fill_buy():
    return BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2024-01-01T00:00:00Z", BacktestOrderSide.BUY, 10.0, 100.0, BacktestFillStatus.FILLED, transaction_cost=1.0)

@pytest.fixture
def fill_sell():
    return BacktestFill("f2", "o2", "s2", "AAPL", "1d", "2024-01-02T00:00:00Z", BacktestOrderSide.SELL, 10.0, 110.0, BacktestFillStatus.FILLED, transaction_cost=1.0)

def test_create_trade_id():
    tid = create_trade_id("AAPL", "2024-01-01", "sig123")
    assert "AAPL" in tid
    assert "2024-01-01" in tid
    assert "sig123" in tid

def test_pair_long_fills(fill_buy, fill_sell):
    closed, open_trades, warnings = pair_long_fills_into_trades([fill_buy, fill_sell])
    assert len(closed) == 1
    assert len(open_trades) == 0
    assert len(warnings) == 0

    trade = closed[0]
    assert trade.symbol == "AAPL"
    assert trade.quantity == 10.0
    assert trade.gross_pnl == 100.0 # (110 - 100) * 10
    assert trade.net_pnl == 98.0 # 100 - 1 - 1
    assert trade.return_pct == 0.1 # 10%

def test_open_trade(fill_buy):
    closed, open_trades, warnings = pair_long_fills_into_trades([fill_buy])
    assert len(closed) == 0
    assert len(open_trades) == 1
    assert len(warnings) == 0

    trade = open_trades[0]
    assert trade.status.value == "OPEN"
    assert trade.net_pnl == -1.0 # Only entry fees

def test_oversell_warning(fill_sell):
    closed, open_trades, warnings = pair_long_fills_into_trades([fill_sell])
    assert len(closed) == 0
    assert len(warnings) == 1
    assert "Oversell" in warnings[0]

def test_build_ledger(fill_buy, fill_sell):
    ledger = build_trade_ledger_from_fills([fill_buy, fill_sell])
    assert len(ledger.trades) == 1
    assert len(ledger.closed_trades) == 1

def test_ledger_to_text(fill_buy, fill_sell):
    ledger = build_trade_ledger_from_fills([fill_buy, fill_sell])
    text = ledger_to_text(ledger)
    assert "Total Trades: 1" in text
    assert "Net PnL: 98.0" in text
