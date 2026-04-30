import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import UniverseSnapshotStatus
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSummary, UniverseValidationReport
from usa_signal_bot.universe.reconciliation import UniverseReconciliationReport
from usa_signal_bot.universe.loader import save_universe_csv
from usa_signal_bot.core.exceptions import UniverseSnapshotError

@dataclass
class UniverseSnapshot:
    snapshot_id: str
    name: str
    status: UniverseSnapshotStatus
    universe_file: str
    symbol_count: int
    active_symbol_count: int
    created_at_utc: str
    summary_file: Optional[str] = None
    validation_file: Optional[str] = None
    reconciliation_file: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

def create_snapshot_id(name: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    clean_name = "".join(c if c.isalnum() else "_" for c in name).lower()
    return f"{clean_name}_{timestamp}"

def build_snapshot_paths(data_root: Path, snapshot_id: str) -> Dict[str, Path]:
    snapshots_dir = data_root / "universe" / "snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    return {
        "metadata": snapshots_dir / f"{snapshot_id}_meta.json",
        "universe": snapshots_dir / f"{snapshot_id}.csv",
        "summary": snapshots_dir / f"{snapshot_id}_summary.json",
        "validation": snapshots_dir / f"{snapshot_id}_validation.json",
        "reconciliation": snapshots_dir / f"{snapshot_id}_reconciliation.json"
    }

def write_universe_snapshot(
    data_root: Path,
    universe: UniverseDefinition,
    summary: Optional[UniverseSummary] = None,
    validation_report: Optional[UniverseValidationReport] = None,
    reconciliation_report: Optional[UniverseReconciliationReport] = None,
    name: str = "expanded_universe"
) -> UniverseSnapshot:

    snapshot_id = create_snapshot_id(name)
    paths = build_snapshot_paths(data_root, snapshot_id)

    # 1. Write Universe CSV
    save_universe_csv(paths["universe"], universe)

    # 2. Write Summary if provided
    if summary:
        from usa_signal_bot.universe.reporting import write_universe_summary_json
        write_universe_summary_json(paths["summary"], summary)

    # 3. Write Validation if provided
    if validation_report:
        with open(paths["validation"], "w") as f:
            import json
            json.dump(validation_report.__dict__, f, indent=2)

    # 4. Write Reconciliation if provided
    if reconciliation_report:
        from usa_signal_bot.universe.reconciliation import write_reconciliation_report_json
        write_reconciliation_report_json(paths["reconciliation"], reconciliation_report)

    # 5. Create Snapshot object
    snapshot = UniverseSnapshot(
        snapshot_id=snapshot_id,
        name=name,
        status=UniverseSnapshotStatus.VALIDATED if validation_report and validation_report.passed else UniverseSnapshotStatus.DRAFT,
        universe_file=str(paths["universe"].relative_to(data_root)),
        summary_file=str(paths["summary"].relative_to(data_root)) if summary else None,
        validation_file=str(paths["validation"].relative_to(data_root)) if validation_report else None,
        reconciliation_file=str(paths["reconciliation"].relative_to(data_root)) if reconciliation_report else None,
        symbol_count=len(universe.symbols),
        active_symbol_count=len(universe.get_active_symbols()),
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

    # 6. Write Metadata
    _write_snapshot_metadata(paths["metadata"], snapshot)

    return snapshot

def _write_snapshot_metadata(path: Path, snapshot: UniverseSnapshot) -> None:
    import tempfile
    import os
    import json

    fd, temp_path_str = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        with open(fd, "w", encoding="utf-8") as f:
            json.dump(snapshot_to_dict(snapshot), f, indent=2)
        os.replace(temp_path, path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise

def read_universe_snapshot(snapshot_file: Path) -> UniverseSnapshot:
    if not snapshot_file.exists():
        raise UniverseSnapshotError(f"Snapshot metadata not found: {snapshot_file}")

    try:
        with open(snapshot_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return UniverseSnapshot(
            snapshot_id=data["snapshot_id"],
            name=data["name"],
            status=UniverseSnapshotStatus(data["status"]),
            universe_file=data["universe_file"],
            symbol_count=data["symbol_count"],
            active_symbol_count=data["active_symbol_count"],
            created_at_utc=data["created_at_utc"],
            summary_file=data.get("summary_file"),
            validation_file=data.get("validation_file"),
            reconciliation_file=data.get("reconciliation_file"),
            metadata=data.get("metadata", {})
        )
    except Exception as e:
        raise UniverseSnapshotError(f"Failed to read snapshot {snapshot_file}: {e}")

def list_universe_snapshots(data_root: Path) -> List[UniverseSnapshot]:
    snapshots_dir = data_root / "universe" / "snapshots"
    if not snapshots_dir.exists() or not snapshots_dir.is_dir():
        return []

    snapshots = []
    for meta_file in snapshots_dir.glob("*_meta.json"):
        try:
            snapshots.append(read_universe_snapshot(meta_file))
        except Exception:
            pass # Skip corrupted

    # Sort by created_at descending
    return sorted(snapshots, key=lambda s: s.created_at_utc, reverse=True)

def get_latest_active_snapshot(data_root: Path) -> Optional[UniverseSnapshot]:
    active_file = data_root / "universe" / "catalog" / "active_snapshot.json"
    if not active_file.exists():
        return None

    try:
        with open(active_file, "r") as f:
            data = json.load(f)
            active_id = data.get("active_snapshot_id")

        if not active_id:
            return None

        paths = build_snapshot_paths(data_root, active_id)
        if paths["metadata"].exists():
            return read_universe_snapshot(paths["metadata"])
    except Exception:
        pass

    return None

def mark_snapshot_active(data_root: Path, snapshot_id: str) -> UniverseSnapshot:
    paths = build_snapshot_paths(data_root, snapshot_id)
    if not paths["metadata"].exists():
        raise UniverseSnapshotError(f"Snapshot {snapshot_id} does not exist")

    # Read, update status, write back
    snapshot = read_universe_snapshot(paths["metadata"])

    # Optional: Archive previously active snapshot
    prev_active = get_latest_active_snapshot(data_root)
    if prev_active and prev_active.snapshot_id != snapshot_id:
        archive_snapshot(data_root, prev_active.snapshot_id)

    snapshot.status = UniverseSnapshotStatus.ACTIVE
    _write_snapshot_metadata(paths["metadata"], snapshot)

    # Update active pointer
    active_file = data_root / "universe" / "catalog" / "active_snapshot.json"
    active_file.parent.mkdir(parents=True, exist_ok=True)

    import tempfile
    import os
    fd, temp_path_str = tempfile.mkstemp(dir=str(active_file.parent), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        with open(fd, "w", encoding="utf-8") as f:
            json.dump({
                "active_snapshot_id": snapshot_id,
                "updated_at_utc": datetime.now(timezone.utc).isoformat()
            }, f, indent=2)
        os.replace(temp_path, active_file)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise

    return snapshot

def archive_snapshot(data_root: Path, snapshot_id: str) -> UniverseSnapshot:
    paths = build_snapshot_paths(data_root, snapshot_id)
    if not paths["metadata"].exists():
        raise UniverseSnapshotError(f"Snapshot {snapshot_id} does not exist")

    snapshot = read_universe_snapshot(paths["metadata"])
    snapshot.status = UniverseSnapshotStatus.ARCHIVED
    _write_snapshot_metadata(paths["metadata"], snapshot)
    return snapshot

def snapshot_to_dict(snapshot: UniverseSnapshot) -> dict:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "name": snapshot.name,
        "status": snapshot.status.value if hasattr(snapshot.status, 'value') else str(snapshot.status),
        "universe_file": snapshot.universe_file,
        "symbol_count": snapshot.symbol_count,
        "active_symbol_count": snapshot.active_symbol_count,
        "created_at_utc": snapshot.created_at_utc,
        "summary_file": snapshot.summary_file,
        "validation_file": snapshot.validation_file,
        "reconciliation_file": snapshot.reconciliation_file,
        "metadata": snapshot.metadata
    }
