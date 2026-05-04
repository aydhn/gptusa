from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime
import json

from usa_signal_bot.core.enums import BenchmarkType, BenchmarkComparisonStatus
from usa_signal_bot.core.exceptions import BacktestMetricError
from usa_signal_bot.backtesting.equity_curve import EquityCurvePoint

@dataclass
class BenchmarkSpec:
    benchmark_id: str
    name: str
    symbol: str
    benchmark_type: BenchmarkType
    description: Optional[str] = None
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BenchmarkSet:
    name: str
    benchmarks: list[BenchmarkSpec]
    created_at_utc: str
    description: Optional[str] = None

@dataclass
class BenchmarkEquityCurve:
    benchmark: BenchmarkSpec
    points: list[EquityCurvePoint]
    starting_cash: float
    ending_equity: Optional[float]
    total_return_pct: Optional[float]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class BenchmarkComparisonReport:
    report_id: str
    created_at_utc: str
    strategy_run_id: Optional[str]
    benchmark_set_name: str
    status: BenchmarkComparisonStatus
    strategy_total_return_pct: Optional[float]
    benchmark_results: list[dict[str, Any]]
    best_benchmark_symbol: Optional[str]
    worst_benchmark_symbol: Optional[str]
    outperformed_count: int
    underperformed_count: int
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def benchmark_spec_to_dict(spec: BenchmarkSpec) -> dict:
    return {
        "benchmark_id": spec.benchmark_id,
        "name": spec.name,
        "symbol": spec.symbol,
        "benchmark_type": spec.benchmark_type.value if hasattr(spec.benchmark_type, "value") else spec.benchmark_type,
        "description": spec.description,
        "enabled": spec.enabled,
        "metadata": spec.metadata
    }

def benchmark_set_to_dict(benchmark_set: BenchmarkSet) -> dict:
    return {
        "name": benchmark_set.name,
        "benchmarks": [benchmark_spec_to_dict(b) for b in benchmark_set.benchmarks],
        "created_at_utc": benchmark_set.created_at_utc,
        "description": benchmark_set.description
    }

def _equity_curve_point_to_dict(p: EquityCurvePoint) -> dict:
    return {
        "timestamp_utc": p.timestamp_utc,
        "equity": p.equity,
        "cash": p.cash,
        "realized_pnl": p.realized_pnl,
        "unrealized_pnl": p.unrealized_pnl,
        "drawdown": p.drawdown,
        "drawdown_pct": p.drawdown_pct
    }

def benchmark_equity_curve_to_dict(curve: BenchmarkEquityCurve) -> dict:
    return {
        "benchmark": benchmark_spec_to_dict(curve.benchmark),
        "points": [_equity_curve_point_to_dict(p) for p in curve.points],
        "starting_cash": curve.starting_cash,
        "ending_equity": curve.ending_equity,
        "total_return_pct": curve.total_return_pct,
        "warnings": curve.warnings,
        "errors": curve.errors
    }

def benchmark_comparison_report_to_dict(report: BenchmarkComparisonReport) -> dict:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "strategy_run_id": report.strategy_run_id,
        "benchmark_set_name": report.benchmark_set_name,
        "status": report.status.value if hasattr(report.status, "value") else report.status,
        "strategy_total_return_pct": report.strategy_total_return_pct,
        "benchmark_results": report.benchmark_results,
        "best_benchmark_symbol": report.best_benchmark_symbol,
        "worst_benchmark_symbol": report.worst_benchmark_symbol,
        "outperformed_count": report.outperformed_count,
        "underperformed_count": report.underperformed_count,
        "warnings": report.warnings,
        "errors": report.errors
    }

def validate_benchmark_spec(spec: BenchmarkSpec) -> None:
    if not spec.benchmark_id:
        raise ValueError("benchmark_id cannot be empty")
    if not spec.name:
        raise ValueError("name cannot be empty")
    if not spec.symbol:
        raise ValueError("symbol cannot be empty")

    valid_types = [t.value for t in BenchmarkType]
    bt_val = spec.benchmark_type.value if hasattr(spec.benchmark_type, "value") else spec.benchmark_type
    if bt_val not in valid_types:
         raise ValueError(f"Invalid benchmark_type: {spec.benchmark_type}")

def validate_benchmark_set(benchmark_set: BenchmarkSet) -> None:
    if not benchmark_set.name:
        raise ValueError("BenchmarkSet name cannot be empty")
    if not benchmark_set.benchmarks:
        raise ValueError("BenchmarkSet must contain at least one benchmark")

    enabled_count = sum(1 for b in benchmark_set.benchmarks if b.enabled)
    if enabled_count == 0:
        raise ValueError("BenchmarkSet must contain at least one enabled benchmark")

    for b in benchmark_set.benchmarks:
        validate_benchmark_spec(b)
