import pytest
from pathlib import Path
from usa_signal_bot.backtesting.backtest_store import (
    backtest_store_dir, build_backtest_run_dir, backtest_store_summary
)
from usa_signal_bot.core.exceptions import BacktestStorageError

def test_backtest_store_dir(tmp_path):
    d = backtest_store_dir(tmp_path)
    assert d.exists()
    assert d.name == "backtests"

def test_build_run_dir(tmp_path):
    d = build_backtest_run_dir(tmp_path, "run1")
    assert d.exists()
    assert d.name == "run1"

def test_build_run_dir_invalid(tmp_path):
    with pytest.raises(BacktestStorageError):
        build_backtest_run_dir(tmp_path, "../run1")

def test_summary_empty(tmp_path):
    summary = backtest_store_summary(tmp_path)
    assert summary["total_runs"] == 0

def test_backtest_store_benchmark_reports(tmp_path):
    from usa_signal_bot.backtesting.backtest_store import (
        write_backtest_benchmark_report, write_backtest_benchmark_table, write_backtest_attribution_report
    )
    from usa_signal_bot.backtesting.benchmark_models import BenchmarkComparisonReport, BenchmarkSet, BenchmarkSpec
    from usa_signal_bot.core.enums import BenchmarkComparisonStatus, BenchmarkType, AttributionStatus, AttributionDimension
    from usa_signal_bot.backtesting.benchmark_comparison import BenchmarkComparisonTable
    from usa_signal_bot.backtesting.performance_attribution import AttributionReport

    rep = BenchmarkComparisonReport(
        "r1", "2024", "run_1", "test", BenchmarkComparisonStatus.OK, 10, [], "SPY", "QQQ", 1, 0
    )
    p = write_backtest_benchmark_report(tmp_path / "rep.json", rep)
    assert p.exists()

    tab = BenchmarkComparisonTable("run_1", [], "2024", BenchmarkComparisonStatus.OK)
    p2 = write_backtest_benchmark_table(tmp_path / "tab.json", tab)
    assert p2.exists()

    attr = AttributionReport("a1", "2024", AttributionStatus.OK, "run_1", [], 100.0, [AttributionDimension.SYMBOL])
    p3 = write_backtest_attribution_report(tmp_path / "attr.json", attr)
    assert p3.exists()
