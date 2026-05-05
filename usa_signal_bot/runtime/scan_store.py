import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.runtime.runtime_models import (
    MarketScanResult, RuntimeState, PipelineStepResult,
    market_scan_result_to_dict, runtime_state_to_dict, pipeline_step_result_to_dict
)
from usa_signal_bot.runtime.runtime_validation import RuntimeValidationReport, runtime_validation_report_to_text

def runtime_store_dir(data_root: Path) -> Path:
    return data_root / "runtime"

def scan_store_dir(data_root: Path) -> Path:
    return runtime_store_dir(data_root) / "scans"

def build_scan_run_dir(data_root: Path, run_id: str) -> Path:
    # Basic path traversal protection
    safe_run_id = run_id.replace("/", "_").replace("\\", "_").replace("..", "_")
    return scan_store_dir(data_root) / safe_run_id

def write_market_scan_result_json(path: Path, result: MarketScanResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(market_scan_result_to_dict(result), f, indent=2)
    return path

def write_runtime_state_json(path: Path, state: RuntimeState) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(runtime_state_to_dict(state), f, indent=2)
    return path

def write_pipeline_step_results_jsonl(path: Path, results: List[PipelineStepResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(pipeline_step_result_to_dict(r)) + "\n")
    return path

def write_scan_manifest_json(path: Path, result: MarketScanResult) -> Path:
    manifest = {
        "run_id": result.run_id,
        "status": result.status.value if hasattr(result.status, "value") else result.status,
        "symbols_count": len(result.resolved_symbols),
        "signal_count": result.signal_count,
        "candidate_count": result.candidate_count,
        "portfolio_allocation_count": result.portfolio_allocation_count,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
    return path

def write_runtime_validation_report_json(path: Path, report: RuntimeValidationReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    report_dict = {
        "valid": report.valid,
        "issue_count": report.issue_count,
        "errors": report.errors,
        "warnings": report.warnings,
        "text": runtime_validation_report_to_text(report)
    }
    with open(path, "w") as f:
        json.dump(report_dict, f, indent=2)
    return path

def read_market_scan_result_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_scan_runs(data_root: Path) -> List[Path]:
    d = scan_store_dir(data_root)
    if not d.exists():
        return []
    return sorted([p for p in d.iterdir() if p.is_dir()], reverse=True)

def get_latest_scan_run_dir(data_root: Path) -> Optional[Path]:
    runs = list_scan_runs(data_root)
    if runs:
        return runs[0]
    return None

def scan_store_summary(data_root: Path) -> Dict[str, Any]:
    runs = list_scan_runs(data_root)
    return {
        "total_runs": len(runs),
        "latest_run": str(runs[0].name) if runs else None
    }
