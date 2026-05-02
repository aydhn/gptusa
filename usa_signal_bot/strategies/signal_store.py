import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from usa_signal_bot.strategies.signal_contract import StrategySignal, signal_to_dict
from usa_signal_bot.strategies.signal_validation import SignalValidationReport
from usa_signal_bot.core.exceptions import SignalStorageError

def signal_store_dir(data_root: Path) -> Path:
    d = data_root / "signals"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_signal_output_filename(strategy_name: str, timeframe: str, run_id: str, fmt: str = "jsonl") -> str:
    # Basic sanitize
    clean_strat = strategy_name.replace("/", "_").replace("\\", "_")
    clean_run = run_id.replace("/", "_").replace("\\", "_")
    return f"{clean_strat}_{timeframe}_{clean_run}.{fmt}"

def build_signal_output_path(data_root: Path, strategy_name: str, timeframe: str, run_id: str, fmt: str = "jsonl") -> Path:
    d = signal_store_dir(data_root)
    filename = build_signal_output_filename(strategy_name, timeframe, run_id, fmt)
    path = d / filename

    # Path traversal check
    if not path.resolve().is_relative_to(d.resolve()):
        raise SignalStorageError(f"Invalid path traversal detected: {path}")

    return path

def write_signals_jsonl(path: Path, signals: List[StrategySignal]) -> Path:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for sig in signals:
                d = signal_to_dict(sig)
                f.write(json.dumps(d) + "\n")
        return path
    except Exception as e:
        raise SignalStorageError(f"Failed to write signals to {path}: {e}")

def read_signals_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise SignalStorageError(f"Signal file does not exist: {path}")

    signals = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    signals.append(json.loads(line))
        return signals
    except Exception as e:
        raise SignalStorageError(f"Failed to read signals from {path}: {e}")

def write_signal_validation_report_json(path: Path, report: SignalValidationReport) -> Path:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        # Convert report to dict manually
        d = {
            "valid": report.valid,
            "total_signals": report.total_signals,
            "valid_signals": report.valid_signals,
            "invalid_signals": report.invalid_signals,
            "issues": [
                {
                    "signal_id": i.signal_id,
                    "symbol": i.symbol,
                    "severity": i.severity,
                    "field": i.field,
                    "message": i.message
                } for i in report.issues
            ],
            "warnings": report.warnings,
            "errors": report.errors
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
        return path
    except Exception as e:
        raise SignalStorageError(f"Failed to write validation report to {path}: {e}")

def list_signal_outputs(data_root: Path) -> List[Path]:
    d = signal_store_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.jsonl")), key=lambda x: x.stat().st_mtime, reverse=True)

def signal_store_summary(data_root: Path) -> Dict[str, Any]:
    files = list_signal_outputs(data_root)
    total_size = sum(f.stat().st_size for f in files)

    return {
        "store_dir": str(signal_store_dir(data_root)),
        "file_count": len(files),
        "total_size_bytes": total_size,
        "latest_file": str(files[0].name) if files else None,
        "latest_file_mtime": files[0].stat().st_mtime if files else None
    }
