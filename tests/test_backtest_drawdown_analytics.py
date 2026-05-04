import pytest
from usa_signal_bot.backtesting.drawdown_analytics import (
    DrawdownAnalytics, calculate_drawdown_analytics, calculate_drawdown_periods,
    drawdown_analytics_to_text
)
from usa_signal_bot.backtesting.equity_curve import EquityCurve, EquityCurvePoint

@pytest.fixture
def empty_curve():
    return EquityCurve([], 100000.0, 100000.0, 0.0, 0.0)

@pytest.fixture
def populated_curve():
    pts = [
        EquityCurvePoint("t1", 100.0, 100.0, 0, 0, 0, 0),
        EquityCurvePoint("t2", 110.0, 110.0, 0, 0, 0, 0), # peak
        EquityCurvePoint("t3", 90.0, 90.0, 0, 0, 0, 0),  # trough
        EquityCurvePoint("t4", 100.0, 100.0, 0, 0, 0, 0),
        EquityCurvePoint("t5", 120.0, 120.0, 0, 0, 0, 0), # recovery & new peak
        EquityCurvePoint("t6", 110.0, 110.0, 0, 0, 0, 0)  # new dd
    ]
    # max_dd_pct would be calculated during build, manually setting for test
    return EquityCurve(pts, 100.0, 110.0, 20.0, 0.1818) # 20 / 110

def test_empty_curve(empty_curve):
    da = calculate_drawdown_analytics(empty_curve)
    assert len(da.warnings) == 1
    assert da.max_drawdown is None

def test_drawdown_periods(populated_curve):
    periods = calculate_drawdown_periods(populated_curve)
    assert len(periods) == 2

    p1 = periods[0]
    assert p1.start_time_utc == "t2"
    assert p1.trough_time_utc == "t3"
    assert p1.recovery_time_utc == "t5"
    assert p1.drawdown == 20.0
    assert p1.recovered is True

    p2 = periods[1]
    assert p2.start_time_utc == "t5"
    assert p2.trough_time_utc == "t6"
    assert p2.recovery_time_utc is None
    assert p2.recovered is False

def test_drawdown_analytics(populated_curve):
    da = calculate_drawdown_analytics(populated_curve)
    assert da.max_drawdown == 20.0
    assert da.max_drawdown_pct == 0.1818
    assert da.recovered_periods == 1
    assert da.unrecovered_periods == 1

def test_drawdown_analytics_to_text(populated_curve):
    da = calculate_drawdown_analytics(populated_curve)
    txt = drawdown_analytics_to_text(da)
    assert "Max Drawdown %:" in txt
    assert "Periods (R/U):    1 / 1" in txt
