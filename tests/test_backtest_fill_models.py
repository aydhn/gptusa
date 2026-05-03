import pytest
from usa_signal_bot.core.enums import BacktestOrderSide, BacktestOrderType, BacktestFillStatus
from usa_signal_bot.core.exceptions import BacktestFillError
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent
from usa_signal_bot.backtesting.fill_models import (
    apply_slippage, calculate_fee, simulate_next_open_fill, validate_fill, BacktestFill
)

def test_apply_slippage():
    assert apply_slippage(100.0, BacktestOrderSide.BUY, 100) == 101.0
    assert apply_slippage(100.0, BacktestOrderSide.SELL, 100) == 99.0

def test_calculate_fee():
    assert calculate_fee(1000.0, 0.01) == 10.0

def test_simulate_next_open_fill():
    order = BacktestOrderIntent("id1", "sig1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, BacktestOrderType.NEXT_OPEN, 10, "")
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="2023", open=100.0, high=105.0, low=95.0, close=102.0, volume=1000)
    fill = simulate_next_open_fill(order, bar, 0.0, 0.0)
    assert fill.fill_price == 100.0
    assert fill.quantity == 10


def test_validate_fill_invalid():
    fill = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, -100.0, BacktestFillStatus.FILLED)
    with pytest.raises(BacktestFillError):
        validate_fill(fill)
