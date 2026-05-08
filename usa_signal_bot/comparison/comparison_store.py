import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import ComparisonStorageError
from usa_signal_bot.storage.file_store import write_json, read_json

from usa_signal_bot.comparison.comparison_models import (
    ComparisonRunResult, MatchedTradePair, PerformanceGapMetrics,
    ExecutionGapMetrics, SignalDriftMetrics, comparison_run_result_to_dict,
    matched_trade_pair_to_dict, performance_gap_metrics_to_dict,
    execution_gap_metrics_to_dict, signal_drift_metrics_to_dict
)

def _write_jsonl(path: Path, data: List[Dict[str, Any]]) -> Path:
    with open(path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')
    return path

def comparison_store_dir(data_root: Path) -> Path:
    d = data_root / "comparison"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_comparison_run_dir(data_root: Path, run_id: str) -> Path:
    if ".." in run_id or "/" in run_id or "\\" in run_id:
        raise ComparisonStorageError("Invalid run_id")
    d = comparison_store_dir(data_root) / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_comparison_result_json(path: Path, result: ComparisonRunResult) -> Path:
    data = comparison_run_result_to_dict(result)
    return write_json(path, data)

def write_matched_trades_jsonl(path: Path, pairs: List[MatchedTradePair]) -> Path:
    data = [matched_trade_pair_to_dict(p) for p in pairs]
    return _write_jsonl(path, data)

def write_performance_gap_json(path: Path, metrics: PerformanceGapMetrics) -> Path:
    data = performance_gap_metrics_to_dict(metrics)
    return write_json(path, data)

def write_execution_gap_json(path: Path, metrics: ExecutionGapMetrics) -> Path:
    data = execution_gap_metrics_to_dict(metrics)
    return write_json(path, data)

def write_signal_drift_json(path: Path, metrics: Optional[SignalDriftMetrics]) -> Path:
    if not metrics:
        return path
    data = signal_drift_metrics_to_dict(metrics)
    return write_json(path, data)

def write_comparison_validation_report_json(path: Path, report: Any) -> Path:
    data = {}
    if hasattr(report, "valid"): data["valid"] = report.valid
    if hasattr(report, "issue_count"): data["issue_count"] = report.issue_count
    if hasattr(report, "issues"):
        data["issues"] = [vars(i) for i in report.issues]
    return write_json(path, data)

def read_comparison_result_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ComparisonStorageError(f"File not found: {path}")
    return read_json(path)

def list_comparison_runs(data_root: Path) -> List[Path]:
    d = comparison_store_dir(data_root)
    return sorted([p for p in d.iterdir() if p.is_dir() and (p / "result.json").exists()], key=lambda x: x.name, reverse=True)

def get_latest_comparison_run_dir(data_root: Path) -> Optional[Path]:
    runs = list_comparison_runs(data_root)
    return runs[0] if runs else None

def comparison_store_summary(data_root: Path) -> Dict[str, Any]:
    runs = list_comparison_runs(data_root)
    return {
        "total_runs": len(runs),
        "latest_run": runs[0].name if runs else None
    }
