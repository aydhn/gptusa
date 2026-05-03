import pytest
from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolioSnapshot
from usa_signal_bot.backtesting.equity_curve import (
    build_equity_curve_from_snapshots, calculate_drawdowns, equity_curve_to_text
)

def test_calculate_drawdowns():
    values = [100.0, 110.0, 105.0, 120.0, 100.0]
    dd = calculate_drawdowns(values)
    # peaks: 100, 110, 110, 120, 120
    # dd: 0, 0, 5, 0, 20
    assert dd[2][0] == 5.0
    assert dd[4][0] == 20.0
    assert round(dd[4][1], 4) == round(20.0/120.0, 4)

def test_build_equity_curve():
    snapshots = [
        BacktestPortfolioSnapshot("2023", 100.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0),
        BacktestPortfolioSnapshot("2023", 100.0, 110.0, 10.0, 0.0, 0.0, 0.0, 0),
        BacktestPortfolioSnapshot("2023", 100.0, 105.0, 5.0, 0.0, 0.0, 0.0, 0)
    ]
    curve = build_equity_curve_from_snapshots(snapshots, 100.0)
    assert len(curve.points) == 3
    assert curve.max_drawdown == 5.0
    assert curve.ending_equity == 105.0

def test_build_empty_curve():
    curve = build_equity_curve_from_snapshots([], 100.0)
    assert len(curve.points) == 0
    assert curve.ending_equity == 100.0

def test_curve_to_text():
    curve = build_equity_curve_from_snapshots([], 100.0)
    txt = equity_curve_to_text(curve)
    assert "Starting Cash:" in txt
