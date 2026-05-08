from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from usa_signal_bot.observability.observability_models import (
    ObservabilityEvent, OperationalMetric, OperationalMetricsSnapshot,
    OperationalHealthReport, LogRotationResult,
    observability_event_to_dict, operational_metric_to_dict,
    operational_metrics_snapshot_to_dict, operational_health_report_to_dict,
    log_rotation_result_to_dict
)

def observability_store_dir(data_root: Path) -> Path:
    p = data_root / "observability"
    p.mkdir(parents=True, exist_ok=True)
    return p

def logs_dir(data_root: Path) -> Path:
    p = observability_store_dir(data_root) / "logs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def metrics_dir(data_root: Path) -> Path:
    p = observability_store_dir(data_root) / "metrics"
    p.mkdir(parents=True, exist_ok=True)
    return p

def reports_dir(data_root: Path) -> Path:
    p = observability_store_dir(data_root) / "reports"
    p.mkdir(parents=True, exist_ok=True)
    return p

def rotation_dir(data_root: Path) -> Path:
    p = observability_store_dir(data_root) / "rotation"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_observability_events_jsonl(path: Path, events: List[ObservabilityEvent]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(observability_event_to_dict(e)) + "\n")
    return path

def write_operational_metrics_jsonl(path: Path, metrics: List[OperationalMetric]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for m in metrics:
            f.write(json.dumps(operational_metric_to_dict(m)) + "\n")
    return path

def write_operational_snapshot_json(path: Path, snapshot: OperationalMetricsSnapshot) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(operational_metrics_snapshot_to_dict(snapshot), f, indent=2)
    return path

def write_operational_health_report_json(path: Path, report: OperationalHealthReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(operational_health_report_to_dict(report), f, indent=2)
    return path

def write_log_rotation_result_json(path: Path, result: LogRotationResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log_rotation_result_to_dict(result), f, indent=2)
    return path

def read_operational_snapshot_json(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_operational_health_report_json(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_observability_reports(data_root: Path) -> List[Path]:
    p = reports_dir(data_root)
    return sorted([x for x in p.iterdir() if x.is_file() and x.suffix == ".json"], key=lambda x: x.stat().st_mtime, reverse=True)

def get_latest_operational_health_report(data_root: Path) -> Optional[Path]:
    p = reports_dir(data_root) / "latest_health.json"
    if p.exists(): return p
    reps = list_observability_reports(data_root)
    for r in reps:
        if r.name.startswith("health_"):
            return r
    return None

def observability_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "logs": len([x for x in logs_dir(data_root).iterdir() if x.is_file()]),
        "metrics": len([x for x in metrics_dir(data_root).iterdir() if x.is_file()]),
        "reports": len([x for x in reports_dir(data_root).iterdir() if x.is_file()]),
        "rotations": len([x for x in rotation_dir(data_root).iterdir() if x.is_file()])
    }
