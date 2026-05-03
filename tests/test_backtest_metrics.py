import pytest
from usa_signal_bot.core.enums import BacktestMetricStatus, BacktestOrderSide, BacktestFillStatus
from usa_signal_bot.backtesting.equity_curve import EquityCurve
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.backtesting.backtest_metrics import (
    calculate_basic_backtest_metrics, estimate_trades_from_fills, backtest_metrics_to_text
)

def test_calculate_metrics_empty():
    curve = EquityCurve([], 100.0, 100.0, 0.0, 0.0)
    metrics = calculate_basic_backtest_metrics(100.0, curve, [])
    assert metrics.status == BacktestMetricStatus.EMPTY
    assert metrics.total_fills == 0
    assert metrics.total_trades == 0

def test_estimate_trades():
    f1 = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)
    f2 = BacktestFill("f2", "o2", "s2", "AAPL", "1d", "2023", BacktestOrderSide.SELL, 10, 110.0, BacktestFillStatus.FILLED)

    trades = estimate_trades_from_fills([f1, f2])
    assert len(trades) == 1
    assert trades[0]["pnl"] == 100.0
    assert trades[0]["is_win"] == True

def test_calculate_metrics_with_trades():
    curve = EquityCurve([], 100.0, 200.0, 0.0, 0.0)
    f1 = BacktestFill("f1", "o1", "s1", "AAPL", "1d", "2023", BacktestOrderSide.BUY, 10, 100.0, BacktestFillStatus.FILLED)
    f2 = BacktestFill("f2", "o2", "s2", "AAPL", "1d", "2023", BacktestOrderSide.SELL, 10, 110.0, BacktestFillStatus.FILLED)
    metrics = calculate_basic_backtest_metrics(100.0, curve, [f1, f2])
    assert metrics.status == BacktestMetricStatus.OK
    assert metrics.total_return == 100.0
    assert metrics.win_rate == 1.0
