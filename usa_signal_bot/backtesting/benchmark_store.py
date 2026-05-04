import json
from pathlib import Path
from typing import Any

from usa_signal_bot.utils.file_utils import safe_mkdir
from usa_signal_bot.core.exceptions import BenchmarkStorageError
from usa_signal_bot.backtesting.benchmark_models import (
    BenchmarkComparisonReport, BenchmarkEquityCurve,
    benchmark_comparison_report_to_dict, benchmark_equity_curve_to_dict
)
from usa_signal_bot.backtesting.benchmark_comparison import BenchmarkComparisonTable, benchmark_comparison_table_to_dict
from usa_signal_bot.backtesting.performance_attribution import AttributionReport, attribution_report_to_dict
from usa_signal_bot.backtesting.buy_and_hold import BuyAndHoldResult, buy_and_hold_result_to_dict

def benchmark_store_dir(data_root: Path) -> Path:
    d = data_root / "backtests" / "benchmarks"
    safe_mkdir(d)
    return d

def build_benchmark_report_dir(data_root: Path, report_id: str) -> Path:
    clean_id = "".join([c for c in report_id if c.isalnum() or c in "-_"])
    d = benchmark_store_dir(data_root) / clean_id
    safe_mkdir(d)
    return d

def _atomic_write_json(path: Path, data: dict) -> Path:
    temp_path = path.with_suffix('.tmp')
    try:
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2)
        temp_path.replace(path)
        return path
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise BenchmarkStorageError(f"Failed to write json to {path}: {e}")

def write_benchmark_comparison_report_json(path: Path, report: BenchmarkComparisonReport) -> Path:
    return _atomic_write_json(path, benchmark_comparison_report_to_dict(report))

def write_benchmark_comparison_table_json(path: Path, table: BenchmarkComparisonTable) -> Path:
    return _atomic_write_json(path, benchmark_comparison_table_to_dict(table))

def write_benchmark_equity_curves_json(path: Path, curves: list[BenchmarkEquityCurve]) -> Path:
    data = {"curves": [benchmark_equity_curve_to_dict(c) for c in curves]}
    return _atomic_write_json(path, data)

def write_buy_and_hold_result_json(path: Path, result: BuyAndHoldResult) -> Path:
    return _atomic_write_json(path, buy_and_hold_result_to_dict(result))

def write_attribution_report_json(path: Path, report: AttributionReport) -> Path:
    return _atomic_write_json(path, attribution_report_to_dict(report))

def list_benchmark_reports(data_root: Path) -> list[Path]:
    d = benchmark_store_dir(data_root)
    if not d.exists():
        return []

    reports = []
    for p in d.iterdir():
        if p.is_dir() and (p / "benchmark_comparison_report.json").exists():
            reports.append(p)
    return sorted(reports, key=lambda x: x.name, reverse=True)

def benchmark_store_summary(data_root: Path) -> dict[str, Any]:
    reports = list_benchmark_reports(data_root)
    return {
        "total_reports": len(reports),
        "latest_report": reports[0].name if reports else None
    }
