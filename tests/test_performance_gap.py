import pytest
from usa_signal_bot.core.enums import GapDirection, GapSeverity, ComparisonMetricStatus
from usa_signal_bot.comparison.performance_gap import (
    calculate_performance_gap_metrics, extract_total_return_pct,
    extract_max_drawdown_pct, extract_win_rate, extract_trade_count,
    calculate_gap_direction, classify_performance_gap_severity,
    performance_gap_metrics_to_text
)

def test_performance_gap_metrics():
    p_data = {"performance": {"total_return_pct": 10.0, "max_drawdown_pct": 5.0, "win_rate": 0.6, "total_trades": 10}}
    b_data = {"metrics": {}, "analytics": {"return_pct": 8.0, "max_drawdown": 6.0, "win_rate_pct": 50.0, "trade_count": 8}}

    res = calculate_performance_gap_metrics(p_data, b_data)

    assert res.status == ComparisonMetricStatus.OK
    assert res.total_return_gap_pct == 2.0
    assert res.drawdown_gap_pct == -1.0
    assert res.win_rate_gap == pytest.approx(0.1)
    assert res.trade_count_gap == 2
    assert res.gap_direction == GapDirection.PAPER_BETTER

def test_gap_direction():
    assert calculate_gap_direction(10, 5, True) == GapDirection.PAPER_BETTER
    assert calculate_gap_direction(5, 10, True) == GapDirection.BACKTEST_BETTER
    assert calculate_gap_direction(10, 10, True) == GapDirection.NEUTRAL

def test_severity_classification():
    p_data = {"performance": {"total_return_pct": 20.0}}
    b_data = {"performance": {"total_return_pct": 5.0}}
    res = calculate_performance_gap_metrics(p_data, b_data)

    sev = classify_performance_gap_severity(res)
    assert sev == GapSeverity.CRITICAL

def test_text_output():
    p_data = {"performance": {"total_return_pct": 10.0}}
    b_data = {"performance": {"total_return_pct": 8.0}}
    res = calculate_performance_gap_metrics(p_data, b_data)
    txt = performance_gap_metrics_to_text(res)
    assert "Return Gap: 2.00%" in txt
