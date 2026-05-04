import pytest
from pathlib import Path
from usa_signal_bot.backtesting.benchmark_store import (
    benchmark_store_dir, build_benchmark_report_dir, write_benchmark_comparison_report_json,
    write_benchmark_comparison_table_json, write_benchmark_equity_curves_json,
    write_buy_and_hold_result_json, write_attribution_report_json,
    list_benchmark_reports, benchmark_store_summary
)
from usa_signal_bot.backtesting.benchmark_models import (
    BenchmarkComparisonReport, BenchmarkSet, BenchmarkSpec, BenchmarkEquityCurve
)
from usa_signal_bot.core.enums import BenchmarkComparisonStatus, BenchmarkType
from usa_signal_bot.backtesting.benchmark_comparison import BenchmarkComparisonTable
from usa_signal_bot.backtesting.performance_attribution import AttributionReport, AttributionStatus
from usa_signal_bot.backtesting.buy_and_hold import BuyAndHoldResult

def test_benchmark_store_paths(tmp_path):
    d = benchmark_store_dir(tmp_path)
    assert d.exists()
    assert d.name == "benchmarks"

    rd = build_benchmark_report_dir(tmp_path, "report_1")
    assert rd.exists()
    assert rd.name == "report_1"

def test_benchmark_store_writes(tmp_path):
    rd = build_benchmark_report_dir(tmp_path, "run_1")

    rep = BenchmarkComparisonReport(
        "r1", "2024", "run_1", "test", BenchmarkComparisonStatus.OK, 10, [], "SPY", "QQQ", 1, 0
    )
    p = write_benchmark_comparison_report_json(rd / "benchmark_comparison_report.json", rep)
    assert p.exists()

    tab = BenchmarkComparisonTable("run_1", [], "2024", BenchmarkComparisonStatus.OK)
    p2 = write_benchmark_comparison_table_json(rd / "benchmark_comparison_table.json", tab)
    assert p2.exists()

    attr = AttributionReport("a1", "2024", AttributionStatus.OK, "run_1", [], 10, [])
    p3 = write_attribution_report_json(rd / "attribution_report.json", attr)
    assert p3.exists()

    spec = BenchmarkSpec("s1", "SPY", "SPY", BenchmarkType.ETF)
    curve = BenchmarkEquityCurve(spec, [], 100, 100, 0)
    p4 = write_benchmark_equity_curves_json(rd / "curves.json", [curve])
    assert p4.exists()

    bh = BuyAndHoldResult("SPY", "1d", 100, 1, 100, 100, 100, 0, 0, curve)
    p5 = write_buy_and_hold_result_json(rd / "bh.json", bh)
    assert p5.exists()

    reports = list_benchmark_reports(tmp_path)
    assert len(reports) == 1

    summary = benchmark_store_summary(tmp_path)
    assert summary["total_reports"] == 1
