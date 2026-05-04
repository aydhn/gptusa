import pytest
from usa_signal_bot.core.enums import BenchmarkType, BenchmarkComparisonStatus, RelativePerformanceBucket
from usa_signal_bot.backtesting.benchmark_models import (
    BenchmarkSpec, BenchmarkSet, BenchmarkEquityCurve, BenchmarkComparisonReport,
    validate_benchmark_spec, validate_benchmark_set,
    benchmark_spec_to_dict, benchmark_set_to_dict,
    benchmark_equity_curve_to_dict, benchmark_comparison_report_to_dict
)
from usa_signal_bot.backtesting.equity_curve import EquityCurvePoint

def test_benchmark_spec_validation():
    valid = BenchmarkSpec("SPY_1", "SPY ETF", "SPY", BenchmarkType.ETF)
    validate_benchmark_spec(valid)

    with pytest.raises(ValueError):
        validate_benchmark_spec(BenchmarkSpec("", "SPY ETF", "SPY", BenchmarkType.ETF))

    with pytest.raises(ValueError):
        validate_benchmark_spec(BenchmarkSpec("SPY_1", "SPY ETF", "", BenchmarkType.ETF))

def test_benchmark_set_validation():
    s1 = BenchmarkSpec("SPY", "SPY", "SPY", BenchmarkType.ETF)
    s2 = BenchmarkSpec("CASH", "CASH", "CASH", BenchmarkType.CASH, enabled=False)

    bset = BenchmarkSet("test", [s1, s2], "2024-01-01T00:00:00Z")
    validate_benchmark_set(bset)

    with pytest.raises(ValueError):
        validate_benchmark_set(BenchmarkSet("", [s1], "2024-01-01T00:00:00Z"))

    with pytest.raises(ValueError):
        validate_benchmark_set(BenchmarkSet("test", [], "2024-01-01T00:00:00Z"))

    with pytest.raises(ValueError):
        validate_benchmark_set(BenchmarkSet("test", [s2], "2024-01-01T00:00:00Z"))

def test_benchmark_models_serialization():
    spec = BenchmarkSpec("SPY", "SPY", "SPY", BenchmarkType.ETF)
    d_spec = benchmark_spec_to_dict(spec)
    assert d_spec["symbol"] == "SPY"

    bset = BenchmarkSet("test", [spec], "2024-01-01T00:00:00Z")
    d_bset = benchmark_set_to_dict(bset)
    assert len(d_bset["benchmarks"]) == 1

    pt = EquityCurvePoint("2024-01-01T00:00:00Z", 1000, 1000, 0, 0, 0, 0)
    curve = BenchmarkEquityCurve(spec, [pt], 1000, 1000, 0.0)
    d_curve = benchmark_equity_curve_to_dict(curve)
    assert d_curve["starting_cash"] == 1000

    report = BenchmarkComparisonReport(
        "report_1", "2024-01-01T00:00:00Z", "run_1", "test", BenchmarkComparisonStatus.OK,
        10.0, [{"symbol": "SPY"}], "SPY", "QQQ", 1, 0
    )
    d_rep = benchmark_comparison_report_to_dict(report)
    assert d_rep["status"] == "OK"
