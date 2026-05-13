from pathlib import Path
from typing import Any, List, Optional, Dict
import json
import datetime

from usa_signal_bot.core.enums import UniverseSnapshotType, SymbolLifecycleSource
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    UniverseSnapshot, create_universe_snapshot_id, validate_universe_snapshot
)
from usa_signal_bot.core.exceptions import UniverseSnapshotError

def build_universe_snapshot(
    universe_name: str,
    symbols: List[str],
    snapshot_type: UniverseSnapshotType,
    as_of_date: Optional[str] = None,
    source: SymbolLifecycleSource = SymbolLifecycleSource.MANUAL_REGISTRY
) -> UniverseSnapshot:

    unique_symbols = sorted(list(set(s.upper() for s in symbols if s)))

    snapshot = UniverseSnapshot(
        snapshot_id=create_universe_snapshot_id(universe_name),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        snapshot_type=snapshot_type,
        as_of_date=as_of_date,
        universe_name=universe_name,
        symbols=unique_symbols,
        source=source,
        symbol_count=len(unique_symbols)
    )
    validate_universe_snapshot(snapshot)
    return snapshot

def load_universe_snapshot_from_json(path: Path) -> UniverseSnapshot:
    if not path.exists() or not path.is_file():
        raise UniverseSnapshotError(f"Snapshot path does not exist: {path}")
    if ".." in str(path):
         raise UniverseSnapshotError("Path traversal detected in snapshot path")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        snapshot = UniverseSnapshot(
            snapshot_id=data.get("snapshot_id", ""),
            created_at_utc=data.get("created_at_utc", ""),
            snapshot_type=UniverseSnapshotType(data.get("snapshot_type", UniverseSnapshotType.UNKNOWN.value)),
            as_of_date=data.get("as_of_date"),
            universe_name=data.get("universe_name", ""),
            symbols=data.get("symbols", []),
            source=SymbolLifecycleSource(data.get("source", SymbolLifecycleSource.UNKNOWN.value)),
            symbol_count=data.get("symbol_count", 0),
            metadata=data.get("metadata", {}),
            warnings=data.get("warnings", []),
            errors=data.get("errors", [])
        )
        validate_universe_snapshot(snapshot)
        return snapshot
    except Exception as e:
        raise UniverseSnapshotError(f"Failed to load universe snapshot from {path}: {e}")

def write_universe_snapshot_example(path: Path) -> Path:
    snapshot = build_universe_snapshot(
        universe_name="example_universe",
        symbols=["AAPL", "MSFT", "TSLA", "DELISTED_CO"],
        snapshot_type=UniverseSnapshotType.HISTORICAL,
        as_of_date="2020-01-01",
        source=SymbolLifecycleSource.MANUAL_REGISTRY
    )
    from usa_signal_bot.universe_lifecycle.lifecycle_models import universe_snapshot_to_dict
    if ".." in str(path):
        raise UniverseSnapshotError("Path traversal detected in snapshot example path")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(universe_snapshot_to_dict(snapshot), f, indent=2)
    return path

def symbols_added_between_snapshots(old: UniverseSnapshot, new: UniverseSnapshot) -> List[str]:
    old_set = set(old.symbols)
    return sorted(list(set(new.symbols) - old_set))

def symbols_removed_between_snapshots(old: UniverseSnapshot, new: UniverseSnapshot) -> List[str]:
    new_set = set(new.symbols)
    return sorted(list(set(old.symbols) - new_set))

def compare_universe_snapshots(old: UniverseSnapshot, new: UniverseSnapshot) -> Dict[str, Any]:
    added = symbols_added_between_snapshots(old, new)
    removed = symbols_removed_between_snapshots(old, new)
    return {
        "old_snapshot_id": old.snapshot_id,
        "new_snapshot_id": new.snapshot_id,
        "old_count": old.symbol_count,
        "new_count": new.symbol_count,
        "added_count": len(added),
        "removed_count": len(removed),
        "added_symbols": added,
        "removed_symbols": removed
    }

def universe_snapshot_to_text(snapshot: UniverseSnapshot) -> str:
    lines = [
        f"Universe Snapshot: {snapshot.universe_name} ({snapshot.snapshot_id})",
        f"Type: {snapshot.snapshot_type.value}",
        f"As Of Date: {snapshot.as_of_date or 'N/A'}",
        f"Source: {snapshot.source.value}",
        f"Symbol Count: {snapshot.symbol_count}",
        f"Note: Snapshot does not guarantee official historical membership."
    ]
    if snapshot.warnings:
        lines.append("Warnings:")
        for w in snapshot.warnings:
            lines.append(f"  - {w}")
    return "\n".join(lines)

def universe_snapshot_diff_to_text(diff: Dict[str, Any]) -> str:
    lines = [
        f"Universe Snapshot Diff",
        f"Old: {diff['old_snapshot_id']} (Count: {diff['old_count']})",
        f"New: {diff['new_snapshot_id']} (Count: {diff['new_count']})",
        f"Added: {diff['added_count']}",
        f"Removed: {diff['removed_count']}"
    ]
    if diff['added_symbols']:
        lines.append(f"Added Symbols: {', '.join(diff['added_symbols'][:20])}" + ("..." if diff['added_count'] > 20 else ""))
    if diff['removed_symbols']:
        lines.append(f"Removed Symbols: {', '.join(diff['removed_symbols'][:20])}" + ("..." if diff['removed_count'] > 20 else ""))
    return "\n".join(lines)
