import pytest
from usa_signal_bot.backtesting.advanced_metrics import (
    calculate_advanced_backtest_metrics, calculate_equity_returns,
    calculate_annualized_return, calculate_sharpe_like_ratio,
    calculate_sortino_like_ratio, advanced_metrics_to_text
)
from usa_signal_bot.backtesting.equity_curve import EquityCurve, EquityCurvePoint
from usa_signal_bot.backtesting.trade_ledger import TradeLedger

@pytest.fixture
def empty_curve():
    return EquityCurve([], 100000.0, 100000.0, 0.0, 0.0)

@pytest.fixture
def empty_ledger():
    return TradeLedger("l1", [], [], [], "now")

@pytest.fixture
def pop_curve():
    pts = [
        EquityCurvePoint("t1", 100.0, 100.0, 0, 0, 0, 0),
        EquityCurvePoint("t2", 110.0, 110.0, 0, 0, 0, 0),
        EquityCurvePoint("t3", 105.0, 105.0, 0, 0, 0, 0),
        EquityCurvePoint("t4", 120.0, 120.0, 0, 0, 0, 0),
    ]
    return EquityCurve(pts, 100.0, 120.0, 5.0, 0.0454)

def test_calculate_equity_returns(pop_curve):
    rets = calculate_equity_returns(pop_curve)
    assert len(rets) == 3
    assert rets[0] == pytest.approx(0.1) # 110 / 100 - 1
    assert rets[1] == pytest.approx((105 - 110) / 110)
    assert rets[2] == pytest.approx((120 - 105) / 105)

def test_annualized_return():
    # 2x return in half a year (126 periods)
    ann = calculate_annualized_return(100.0, 200.0, 126, 252)
    assert ann == pytest.approx(3.0) # 2^2 - 1 = 3 (300%)

def test_sharpe_like():
    rets = [0.01, 0.02, -0.01, 0.01]
    sharpe = calculate_sharpe_like_ratio(rets, 252)
    assert sharpe is not None

    # 0 std dev
    sharpe0 = calculate_sharpe_like_ratio([0.01, 0.01], 252)
    assert sharpe0 is None

def test_sortino_like():
    rets = [0.01, 0.02, -0.01, -0.02]
    sortino = calculate_sortino_like_ratio(rets, 252)
    assert sortino is not None

    # No downside
    sortino0 = calculate_sortino_like_ratio([0.01, 0.02], 252)
    assert sortino0 is None

def test_advanced_metrics_empty(empty_curve, empty_ledger):
    metrics = calculate_advanced_backtest_metrics(100000.0, empty_curve, empty_ledger)
    assert metrics.status.value == "EMPTY"
    assert metrics.annualized_return_pct is None

def test_advanced_metrics_populated(pop_curve, empty_ledger):
    metrics = calculate_advanced_backtest_metrics(100.0, pop_curve, empty_ledger)
    assert metrics.status.value in ["OK", "WARNING"]
    assert metrics.total_return_pct == 0.2
    assert metrics.annualized_return_pct is not None
    assert metrics.sharpe_like_ratio is not None

def test_advanced_metrics_to_text(pop_curve, empty_ledger):
    metrics = calculate_advanced_backtest_metrics(100.0, pop_curve, empty_ledger)
    txt = advanced_metrics_to_text(metrics)
    assert "Total Return %:     20.00%" in txt
