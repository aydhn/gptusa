from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from pathlib import Path

from usa_signal_bot.core.enums import ComparisonSourceType
from usa_signal_bot.comparison.comparison_models import ComparisonSourceSummary
from usa_signal_bot.storage.file_store import read_json, read_jsonl
from usa_signal_bot.core.exceptions import ResultLoaderError

@dataclass
class LoadedComparisonData:
    source_summary: ComparisonSourceSummary
    records: Dict[str, Any]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def load_paper_run_for_comparison(path: Path) -> LoadedComparisonData:
    if not path.exists():
        raise ResultLoaderError(f"Paper run path does not exist: {path}")

    records = {}
    warnings = []
    errors = []

    trades_path = path / "paper_trades.jsonl"
    orders_path = path / "paper_orders.jsonl"
    fills_path = path / "paper_fills.jsonl"
    report_path = path / "performance_report.json"
    analytics_path = path / "analytics_result.json"

    if trades_path.exists():
        records["trades"] = read_jsonl(trades_path)
    if orders_path.exists():
        records["orders"] = read_jsonl(orders_path)
    if fills_path.exists():
        records["fills"] = read_jsonl(fills_path)
    if report_path.exists():
        records["performance"] = read_json(report_path)
    if analytics_path.exists():
        records["analytics"] = read_json(analytics_path)

    trades = records.get("trades", [])
    symbols = list(set([t.get("symbol") for t in trades if t.get("symbol")]))
    timeframes = list(set([t.get("timeframe", "1d") for t in trades]))

    summary = ComparisonSourceSummary(
        source_type=ComparisonSourceType.PAPER_RUN,
        source_id=path.name,
        source_path=str(path),
        record_count=len(trades),
        symbols=symbols,
        timeframes=timeframes,
        warnings=warnings,
        errors=errors
    )
    return LoadedComparisonData(summary, records, warnings, errors)

def load_backtest_run_for_comparison(path: Path) -> LoadedComparisonData:
    if not path.exists():
        raise ResultLoaderError(f"Backtest run path does not exist: {path}")

    records = {}
    warnings = []
    errors = []

    trades_path = path / "trades.jsonl"
    orders_path = path / "orders.jsonl"
    fills_path = path / "fills.jsonl"
    metrics_path = path / "metrics.json"

    if trades_path.exists():
        records["trades"] = read_jsonl(trades_path)
    if orders_path.exists():
        records["orders"] = read_jsonl(orders_path)
    if fills_path.exists():
        records["fills"] = read_jsonl(fills_path)
    if metrics_path.exists():
        records["performance"] = read_json(metrics_path)

    trades = records.get("trades", [])
    symbols = list(set([t.get("symbol") for t in trades if t.get("symbol")]))
    timeframes = list(set([t.get("timeframe", "1d") for t in trades]))

    summary = ComparisonSourceSummary(
        source_type=ComparisonSourceType.BACKTEST_RUN,
        source_id=path.name,
        source_path=str(path),
        record_count=len(trades),
        symbols=symbols,
        timeframes=timeframes,
        warnings=warnings,
        errors=errors
    )
    return LoadedComparisonData(summary, records, warnings, errors)

def load_basket_run_for_comparison(path: Path) -> LoadedComparisonData:
    if not path.exists():
        raise ResultLoaderError(f"Basket run path does not exist: {path}")

    records = {}
    warnings = []
    errors = []

    trades_path = path / "basket_trades.jsonl"
    report_path = path / "basket_report.json"

    if trades_path.exists():
        records["trades"] = read_jsonl(trades_path)
    if report_path.exists():
        records["performance"] = read_json(report_path)

    trades = records.get("trades", [])
    symbols = list(set([t.get("symbol") for t in trades if t.get("symbol")]))
    timeframes = list(set([t.get("timeframe", "1d") for t in trades]))

    summary = ComparisonSourceSummary(
        source_type=ComparisonSourceType.BASKET_BACKTEST_RUN,
        source_id=path.name,
        source_path=str(path),
        record_count=len(trades),
        symbols=symbols,
        timeframes=timeframes,
        warnings=warnings,
        errors=errors
    )
    return LoadedComparisonData(summary, records, warnings, errors)

def load_scan_run_for_comparison(path: Path) -> LoadedComparisonData:
    if not path.exists():
        raise ResultLoaderError(f"Scan run path does not exist: {path}")

    records = {}
    warnings = []
    errors = []

    signals_path = path / "signals.jsonl"
    candidates_path = path / "candidates.jsonl"

    if signals_path.exists():
        records["signals"] = read_jsonl(signals_path)
    if candidates_path.exists():
        records["candidates"] = read_jsonl(candidates_path)

    signals = records.get("signals", [])
    symbols = list(set([s.get("symbol") for s in signals if s.get("symbol")]))
    timeframes = list(set([s.get("timeframe", "1d") for s in signals]))

    summary = ComparisonSourceSummary(
        source_type=ComparisonSourceType.SCAN_RUN,
        source_id=path.name,
        source_path=str(path),
        record_count=len(signals),
        symbols=symbols,
        timeframes=timeframes,
        warnings=warnings,
        errors=errors
    )
    return LoadedComparisonData(summary, records, warnings, errors)

def load_signal_file_for_drift(path: Path) -> LoadedComparisonData:
    if not path.exists():
        raise ResultLoaderError(f"Signal file does not exist: {path}")

    records = {"signals": read_jsonl(path)}
    signals = records["signals"]
    symbols = list(set([s.get("symbol") for s in signals if s.get("symbol")]))
    timeframes = list(set([s.get("timeframe", "1d") for s in signals]))

    summary = ComparisonSourceSummary(
        source_type=ComparisonSourceType.SIGNAL_FILE,
        source_id=path.name,
        source_path=str(path),
        record_count=len(signals),
        symbols=symbols,
        timeframes=timeframes,
        warnings=[],
        errors=[]
    )
    return LoadedComparisonData(summary, records, [], [])

def load_candidate_file_for_drift(path: Path) -> LoadedComparisonData:
    if not path.exists():
        raise ResultLoaderError(f"Candidate file does not exist: {path}")

    records = {"candidates": read_jsonl(path)}
    candidates = records["candidates"]
    symbols = list(set([c.get("symbol") for c in candidates if c.get("symbol")]))
    timeframes = list(set([c.get("timeframe", "1d") for c in candidates]))

    summary = ComparisonSourceSummary(
        source_type=ComparisonSourceType.CANDIDATE_FILE,
        source_id=path.name,
        source_path=str(path),
        record_count=len(candidates),
        symbols=symbols,
        timeframes=timeframes,
        warnings=[],
        errors=[]
    )
    return LoadedComparisonData(summary, records, [], [])

def infer_symbols_from_records(records: Dict[str, Any]) -> List[str]:
    symbols = set()
    for key in ["trades", "orders", "fills", "signals", "candidates"]:
        for item in records.get(key, []):
            if isinstance(item, dict) and item.get("symbol"):
                symbols.add(item["symbol"])
    return list(symbols)

def infer_timeframes_from_records(records: Dict[str, Any]) -> List[str]:
    timeframes = set()
    for key in ["trades", "orders", "fills", "signals", "candidates"]:
        for item in records.get(key, []):
            if isinstance(item, dict) and item.get("timeframe"):
                timeframes.add(item["timeframe"])
    return list(timeframes) if timeframes else ["1d"]

def normalize_trade_records(records: Dict[str, Any], source_type: ComparisonSourceType) -> List[Dict[str, Any]]:
    return records.get("trades", [])

def normalize_order_records(records: Dict[str, Any], source_type: ComparisonSourceType) -> List[Dict[str, Any]]:
    return records.get("orders", [])

def normalize_fill_records(records: Dict[str, Any], source_type: ComparisonSourceType) -> List[Dict[str, Any]]:
    return records.get("fills", [])

def normalize_signal_records(records: Dict[str, Any], source_type: ComparisonSourceType) -> List[Dict[str, Any]]:
    return records.get("signals", [])
