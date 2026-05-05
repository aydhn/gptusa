import json
from pathlib import Path
from typing import Any

from usa_signal_bot.risk.risk_models import (
    RiskDecision,
    RiskRunResult,
    risk_decision_to_dict,
    risk_run_result_to_dict
)
from usa_signal_bot.risk.exposure_guard import ExposureSnapshot, exposure_snapshot_to_dict
from usa_signal_bot.risk.risk_validation import RiskValidationReport
from usa_signal_bot.core.exceptions import RiskStorageError

def risk_store_dir(data_root: Path) -> Path:
    d = data_root / "risk"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_risk_run_dir(data_root: Path, run_id: str) -> Path:
    safe_id = "".join([c for c in run_id if c.isalnum() or c in "-_"])
    d = risk_store_dir(data_root) / safe_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_risk_run_result_json(path: Path, result: RiskRunResult) -> Path:
    try:
        p = path / "result.json"
        with open(p, "w", encoding="utf-8") as f:
            json.dump(risk_run_result_to_dict(result), f, indent=2)
        return p
    except Exception as e:
        raise RiskStorageError(f"Failed to write risk run result: {e}")

def write_risk_decisions_jsonl(path: Path, decisions: list[RiskDecision]) -> Path:
    try:
        p = path / "decisions.jsonl"
        with open(p, "w", encoding="utf-8") as f:
            for d in decisions:
                f.write(json.dumps(risk_decision_to_dict(d)) + "\n")
        return p
    except Exception as e:
        raise RiskStorageError(f"Failed to write decisions JSONL: {e}")

def write_exposure_snapshot_json(path: Path, snapshot: ExposureSnapshot) -> Path:
    try:
        p = path / "exposure_snapshot.json"
        with open(p, "w", encoding="utf-8") as f:
            json.dump(exposure_snapshot_to_dict(snapshot), f, indent=2)
        return p
    except Exception as e:
        raise RiskStorageError(f"Failed to write exposure snapshot: {e}")

def write_risk_validation_report_json(path: Path, report: RiskValidationReport) -> Path:
    try:
        p = path / "validation_report.json"
        with open(p, "w", encoding="utf-8") as f:
            data = {
                "valid": report.valid,
                "issue_count": report.issue_count,
                "warning_count": report.warning_count,
                "error_count": report.error_count,
                "issues": [i.__dict__ for i in report.issues],
                "warnings": report.warnings,
                "errors": report.errors
            }
            json.dump(data, f, indent=2)
        return p
    except Exception as e:
        raise RiskStorageError(f"Failed to write validation report: {e}")

def read_risk_run_result_json(path: Path) -> dict[str, Any]:
    p = path / "result.json"
    if not p.exists():
        raise RiskStorageError(f"Result file not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def read_risk_decisions_jsonl(path: Path) -> list[dict[str, Any]]:
    p = path / "decisions.jsonl"
    if not p.exists():
        return []
    res = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def list_risk_runs(data_root: Path) -> list[Path]:
    d = risk_store_dir(data_root)
    if not d.exists():
        return []
    runs = [p for p in d.iterdir() if p.is_dir()]
    return sorted(runs, key=lambda x: x.name, reverse=True)

def get_latest_risk_run_dir(data_root: Path) -> Path | None:
    runs = list_risk_runs(data_root)
    return runs[0] if runs else None

def risk_store_summary(data_root: Path) -> dict[str, Any]:
    runs = list_risk_runs(data_root)
    return {
        "total_runs": len(runs),
        "latest_run": runs[0].name if runs else None
    }
