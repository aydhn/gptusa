import pytest
from usa_signal_bot.backtesting.benchmark_reporting import (
    benchmark_set_to_text, benchmark_equity_curve_to_text,
    benchmark_comparison_report_to_text, buy_and_hold_result_to_text,
    attribution_report_to_text, full_benchmark_analysis_to_text
)
from usa_signal_bot.backtesting.benchmark_models import BenchmarkSet, BenchmarkSpec, BenchmarkEquityCurve, BenchmarkComparisonReport
from usa_signal_bot.core.enums import BenchmarkType, BenchmarkComparisonStatus, AttributionStatus, AttributionDimension
from usa_signal_bot.backtesting.benchmark_comparison import BenchmarkComparisonTable
from usa_signal_bot.backtesting.buy_and_hold import BuyAndHoldResult
from usa_signal_bot.backtesting.performance_attribution import AttributionReport

def test_benchmark_set_to_text():
    spec = BenchmarkSpec("SPY", "SPY", "SPY", BenchmarkType.ETF)
    bset = BenchmarkSet("test", [spec], "2024-01-01T00:00:00Z", "desc")
    txt = benchmark_set_to_text(bset)
    assert "SPY" in txt
    assert "desc" in txt

def test_benchmark_equity_curve_to_text():
    spec = BenchmarkSpec("SPY", "SPY", "SPY", BenchmarkType.ETF)
    curve = BenchmarkEquityCurve(spec, [], 1000.0, 1100.0, 10.0)
    txt = benchmark_equity_curve_to_text(curve)
    assert "1000.00" in txt
    assert "1100.00" in txt
    assert "10.00%" in txt

def test_benchmark_comparison_report_to_text():
    rep = BenchmarkComparisonReport(
        "r1", "2024", "run_1", "test", BenchmarkComparisonStatus.OK, 10.0, [], "SPY", "QQQ", 1, 0
    )
    txt = benchmark_comparison_report_to_text(rep)
    assert "10.00%" in txt
    assert "SPY" in txt

def test_buy_and_hold_result_to_text():
    spec = BenchmarkSpec("SPY", "SPY", "SPY", BenchmarkType.ETF)
    curve = BenchmarkEquityCurve(spec, [], 1000.0, 1100.0, 10.0)
    bh = BuyAndHoldResult("SPY", "1d", 1000.0, 10.0, 100.0, 110.0, 1100.0, 100.0, 10.0, curve)
    txt = buy_and_hold_result_to_text(bh)
    assert "1000.00" in txt
    assert "10.00%" in txt

def test_attribution_report_to_text():
    attr = AttributionReport("a1", "2024", AttributionStatus.OK, "run_1", [], 100.0, [AttributionDimension.SYMBOL])
    txt = attribution_report_to_text(attr)
    assert "EMPTY" in txt

def test_full_benchmark_analysis_to_text():
    tab = BenchmarkComparisonTable("run_1", [], "2024", BenchmarkComparisonStatus.OK)
    attr = AttributionReport("a1", "2024", AttributionStatus.OK, "run_1", [], 100.0, [AttributionDimension.SYMBOL])
    txt = full_benchmark_analysis_to_text(tab, attr)
    assert "No benchmark comparisons available" in txt
    assert "Performance Attribution" in txt
