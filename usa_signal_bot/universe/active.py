import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List

from usa_signal_bot.core.enums import ActiveUniverseSource
from usa_signal_bot.core.exceptions import ActiveUniverseResolutionError
from usa_signal_bot.universe.models import UniverseDefinition
from usa_signal_bot.universe.loader import load_universe_csv, load_default_watchlist
from usa_signal_bot.universe.snapshots import get_latest_active_snapshot, list_universe_snapshots, read_universe_snapshot

@dataclass
class ActiveUniverseResolution:
    source: ActiveUniverseSource
    universe: UniverseDefinition
    source_path: Optional[str]
    snapshot_id: Optional[str]
    symbol_count: int
    active_symbol_count: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def load_universe_from_explicit_file(path: Path) -> ActiveUniverseResolution:
    if not path.is_absolute():
        raise ActiveUniverseResolutionError(f"Explicit file path must be absolute: {path}")
    if not path.exists() or not path.is_file():
        raise ActiveUniverseResolutionError(f"Explicit file not found: {path}")

    # Path traversal check
    if ".." in str(path) or str(path).startswith("http"):
        raise ActiveUniverseResolutionError(f"Invalid explicit file path: {path}")

    load_result = load_universe_csv(path)

    return ActiveUniverseResolution(
        source=ActiveUniverseSource.EXPLICIT_FILE,
        universe=load_result.universe,
        source_path=str(path),
        snapshot_id=None,
        symbol_count=len(load_result.universe.symbols),
        active_symbol_count=len(load_result.universe.get_active_symbols()),
        warnings=load_result.warnings,
        errors=load_result.errors
    )

def load_universe_from_active_snapshot(data_root: Path) -> ActiveUniverseResolution:
    snapshot = get_latest_active_snapshot(data_root)
    if not snapshot:
        raise ActiveUniverseResolutionError("No active snapshot found")

    universe_path = data_root / snapshot.universe_file
    if not universe_path.exists():
        raise ActiveUniverseResolutionError(f"Active snapshot universe file not found: {universe_path}")

    load_result = load_universe_csv(universe_path)

    return ActiveUniverseResolution(
        source=ActiveUniverseSource.ACTIVE_SNAPSHOT,
        universe=load_result.universe,
        source_path=str(universe_path),
        snapshot_id=snapshot.snapshot_id,
        symbol_count=len(load_result.universe.symbols),
        active_symbol_count=len(load_result.universe.get_active_symbols()),
        warnings=load_result.warnings,
        errors=load_result.errors
    )

def load_universe_from_latest_snapshot(data_root: Path) -> ActiveUniverseResolution:
    snapshots = list_universe_snapshots(data_root)
    if not snapshots:
        raise ActiveUniverseResolutionError("No snapshots found")

    snapshot = snapshots[0]
    universe_path = data_root / snapshot.universe_file
    if not universe_path.exists():
        raise ActiveUniverseResolutionError(f"Latest snapshot universe file not found: {universe_path}")

    load_result = load_universe_csv(universe_path)

    return ActiveUniverseResolution(
        source=ActiveUniverseSource.LATEST_SNAPSHOT,
        universe=load_result.universe,
        source_path=str(universe_path),
        snapshot_id=snapshot.snapshot_id,
        symbol_count=len(load_result.universe.symbols),
        active_symbol_count=len(load_result.universe.get_active_symbols()),
        warnings=load_result.warnings,
        errors=load_result.errors
    )

def load_universe_from_default_watchlist(data_root: Path) -> ActiveUniverseResolution:
    try:
        load_result = load_default_watchlist(data_root)

        return ActiveUniverseResolution(
            source=ActiveUniverseSource.DEFAULT_WATCHLIST,
            universe=load_result.universe,
            source_path=load_result.source_path,
            snapshot_id=None,
            symbol_count=len(load_result.universe.symbols),
            active_symbol_count=len(load_result.universe.get_active_symbols()),
            warnings=load_result.warnings,
            errors=load_result.errors
        )
    except Exception as e:
        raise ActiveUniverseResolutionError(f"Failed to load default watchlist: {e}")

def resolve_active_universe(data_root: Path, explicit_file: Optional[Path] = None, fallback_to_watchlist: bool = True) -> ActiveUniverseResolution:
    if explicit_file:
        return load_universe_from_explicit_file(explicit_file)

    warnings = []

    try:
        res = load_universe_from_active_snapshot(data_root)
        return res
    except ActiveUniverseResolutionError as e:
        warnings.append(f"Could not load from active snapshot: {e}")

    try:
        res = load_universe_from_latest_snapshot(data_root)
        res.warnings.extend(warnings)
        return res
    except ActiveUniverseResolutionError as e:
        warnings.append(f"Could not load from latest snapshot: {e}")

    if fallback_to_watchlist:
        try:
            res = load_universe_from_default_watchlist(data_root)
            res.warnings.extend(warnings)
            return res
        except ActiveUniverseResolutionError as e:
            warnings.append(f"Could not load from default watchlist: {e}")

    raise ActiveUniverseResolutionError(f"Failed to resolve active universe. Warnings: {warnings}")


def active_universe_resolution_to_text(resolution: ActiveUniverseResolution) -> str:
    lines = [
        "=== Active Universe Resolution ===",
        f"Source              : {resolution.source.value if hasattr(resolution.source, 'value') else str(resolution.source)}",
        f"Source Path         : {resolution.source_path}",
        f"Snapshot ID         : {resolution.snapshot_id or 'N/A'}",
        f"Total Symbols       : {resolution.symbol_count}",
        f"Active Symbols      : {resolution.active_symbol_count}"
    ]

    if resolution.warnings:
        lines.append("\nWarnings:")
        for w in resolution.warnings:
            lines.append(f" - {w}")

    if resolution.errors:
        lines.append("\nErrors:")
        for e in resolution.errors:
            lines.append(f" - {e}")

    return "\n".join(lines)


def write_active_universe_resolution_json(path: Path, resolution: ActiveUniverseResolution) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "source": resolution.source.value if hasattr(resolution.source, 'value') else str(resolution.source),
        "universe_name": resolution.universe.name,
        "source_path": resolution.source_path,
        "snapshot_id": resolution.snapshot_id,
        "symbol_count": resolution.symbol_count,
        "active_symbol_count": resolution.active_symbol_count,
        "warnings": resolution.warnings,
        "errors": resolution.errors
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path
