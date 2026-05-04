"""Storage management for backtest runs."""
from pathlib import Path
from typing import Any
import json
import os
from datetime import datetime


from usa_signal_bot.core.exceptions import BacktestStorageError
from usa_signal_bot.backtesting.backtest_engine import BacktestRunResult
from usa_signal_bot.backtesting.event_models import BacktestEvent, event_to_dict
from usa_signal_bot.backtesting.fill_models import BacktestFill, fill_to_dict
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent, order_intent_to_dict
from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolioSnapshot, portfolio_snapshot_to_dict
from usa_signal_bot.backtesting.equity_curve import EquityCurve, equity_curve_to_dict
from usa_signal_bot.backtesting.backtest_metrics import BacktestMetrics, backtest_metrics_to_dict


def save_json(data: Any, path: Path) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def save_jsonl(data_list: list[Any], path: Path) -> None:
    with open(path, "w") as f:
        for item in data_list:
            f.write(json.dumps(item) + "\n")

def load_json(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def backtest_store_dir(data_root: Path) -> Path:
    d = data_root / "backtests"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_backtest_run_dir(data_root: Path, run_id: str) -> Path:
    if ".." in run_id or "/" in run_id or "\\" in run_id:
        raise BacktestStorageError("Invalid run_id")

    d = backtest_store_dir(data_root) / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_backtest_result_json(path: Path, result: BacktestRunResult) -> Path:
    d = {
        "run_id": result.run_id,
        "run_name": result.run_name,
        "status": result.status.value,
        "created_at_utc": result.created_at_utc,
        "warnings": result.warnings,
        "errors": result.errors,
        "request": {
            "run_name": result.request.run_name,
            "symbols": result.request.symbols,
            "timeframe": result.request.timeframe,
            "signal_file": result.request.signal_file,
            "selected_candidates_file": result.request.selected_candidates_file
        }
    }
    save_json(d, path)
    return path

def write_backtest_events_jsonl(path: Path, events: list[BacktestEvent]) -> Path:
    dicts = [event_to_dict(e) for e in events]
    save_jsonl(dicts, path)
    return path

def write_backtest_fills_jsonl(path: Path, fills: list[BacktestFill]) -> Path:
    dicts = [fill_to_dict(f) for f in fills]
    save_jsonl(dicts, path)
    return path

def write_backtest_orders_jsonl(path: Path, orders: list[BacktestOrderIntent]) -> Path:
    dicts = [order_intent_to_dict(o) for o in orders]
    save_jsonl(dicts, path)
    return path

def write_backtest_snapshots_jsonl(path: Path, snapshots: list[BacktestPortfolioSnapshot]) -> Path:
    dicts = [portfolio_snapshot_to_dict(s) for s in snapshots]
    save_jsonl(dicts, path)
    return path

def write_equity_curve_jsonl(path: Path, curve: EquityCurve) -> Path:
    d = equity_curve_to_dict(curve)
    save_json(d, path)
    return path

def write_backtest_metrics_json(path: Path, metrics: BacktestMetrics) -> Path:
    d = backtest_metrics_to_dict(metrics)
    save_json(d, path)
    return path

def list_backtest_runs(data_root: Path) -> list[Path]:
    store_dir = backtest_store_dir(data_root)
    runs = []
    for d in store_dir.iterdir():
        if d.is_dir() and (d / "result.json").exists():
            runs.append(d)
    runs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return runs

def backtest_store_summary(data_root: Path) -> dict[str, Any]:
    runs = list_backtest_runs(data_root)
    summary = {
        "total_runs": len(runs),
        "latest_run_id": runs[0].name if runs else None,
        "latest_run_time": datetime.fromtimestamp(runs[0].stat().st_mtime).isoformat() if runs else None
    }
    return summary

def write_backtest_benchmark_report(path: Path, report: Any) -> Path:
    from usa_signal_bot.backtesting.benchmark_models import benchmark_comparison_report_to_dict
    save_json(benchmark_comparison_report_to_dict(report), path)
    return path

def write_backtest_benchmark_table(path: Path, table: Any) -> Path:
    from usa_signal_bot.backtesting.benchmark_store import write_benchmark_comparison_table_json
    return write_benchmark_comparison_table_json(path, table)

def write_backtest_attribution_report(path: Path, report: Any) -> Path:
    from usa_signal_bot.backtesting.benchmark_store import write_attribution_report_json
    return write_attribution_report_json(path, report)
