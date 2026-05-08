import json
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime, timezone

from usa_signal_bot.regression.regression_models import (
    GoldenSnapshot,
    RegressionArtifactType,
    create_golden_snapshot_id,
    golden_snapshot_to_dict
)

def create_golden_snapshot(name: str, payload: Dict[str, Any], artifact_type: RegressionArtifactType = RegressionArtifactType.SNAPSHOT) -> GoldenSnapshot:
    normalized_payload = normalize_payload_for_snapshot(payload)
    checksum = stable_payload_checksum(normalized_payload)
    return GoldenSnapshot(
        snapshot_id=create_golden_snapshot_id(name),
        name=name,
        artifact_type=artifact_type,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        checksum=checksum,
        payload=normalized_payload
    )

def stable_payload_checksum(payload: Any) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def normalize_payload_for_snapshot(payload: Any) -> Any:
    volatile_keys = {"run_id", "created_at_utc", "started_at_utc", "completed_at_utc", "duration_seconds", "timestamp", "snapshot_id"}

    if isinstance(payload, dict):
        normalized = {}
        for k, v in payload.items():
            if k in volatile_keys:
                continue
            normalized[k] = normalize_payload_for_snapshot(v)
        return normalized
    elif isinstance(payload, list):
        return [normalize_payload_for_snapshot(item) for item in payload]
    else:
        return payload

def write_golden_snapshot_json(path: Path, snapshot: GoldenSnapshot) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(golden_snapshot_to_dict(snapshot), f, indent=2)
    return path

def read_golden_snapshot_json(path: Path) -> GoldenSnapshot:
    with open(path, "r") as f:
        data = json.load(f)
    return GoldenSnapshot(
        snapshot_id=data["snapshot_id"],
        name=data["name"],
        artifact_type=RegressionArtifactType(data["artifact_type"]),
        created_at_utc=data["created_at_utc"],
        checksum=data["checksum"],
        payload=data["payload"],
        metadata=data.get("metadata", {})
    )

def compare_golden_snapshots(baseline: Optional[GoldenSnapshot], current: Optional[GoldenSnapshot]) -> Dict[str, Any]:
    if baseline is None and current is None:
        return {"status": "INVALID", "message": "Both snapshots missing"}
    if baseline is None:
        return {"status": "MISSING_BASELINE", "message": "No baseline to compare against"}
    if current is None:
        return {"status": "MISSING_CURRENT", "message": "Current snapshot is missing"}

    match = baseline.checksum == current.checksum
    status = "MATCH" if match else "DRIFT"
    diff_summary = {} if match else snapshot_diff_summary(baseline.payload, current.payload)

    return {
        "status": status,
        "baseline_checksum": baseline.checksum,
        "current_checksum": current.checksum,
        "diff_summary": diff_summary
    }

def snapshot_diff_summary(baseline_payload: Dict[str, Any], current_payload: Dict[str, Any], max_diffs: int = 50) -> Dict[str, Any]:
    diffs = []

    b_keys = set(baseline_payload.keys())
    c_keys = set(current_payload.keys())

    added = c_keys - b_keys
    removed = b_keys - c_keys
    common = b_keys & c_keys

    for k in added:
        diffs.append(f"Added key: {k}")
    for k in removed:
         diffs.append(f"Removed key: {k}")

    for k in common:
        if baseline_payload[k] != current_payload[k]:
             diffs.append(f"Modified key: {k}")
             if len(diffs) >= max_diffs:
                 diffs.append("... max diffs reached")
                 break

    return {"diff_count": len(diffs), "details": diffs}

def load_baseline_snapshot(snapshot_dir: Path, name: str) -> Optional[GoldenSnapshot]:
    path = snapshot_dir / f"{name}_baseline.json"
    if path.exists():
        return read_golden_snapshot_json(path)
    return None

def write_or_update_baseline_snapshot(snapshot_dir: Path, snapshot: GoldenSnapshot, update: bool = False) -> Path:
    path = snapshot_dir / f"{snapshot.name}_baseline.json"
    if path.exists() and not update:
        return path
    return write_golden_snapshot_json(path, snapshot)
