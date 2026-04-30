import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from usa_signal_bot.core.enums import UniverseLayer, UniverseSourceType
from usa_signal_bot.core.exceptions import UniverseCatalogError

@dataclass
class UniverseCatalogEntry:
    entry_id: str
    name: str
    layer: UniverseLayer
    source_type: UniverseSourceType
    path: str
    active: bool
    created_at_utc: str
    symbol_count: Optional[int] = None
    notes: Optional[str] = None

@dataclass
class UniverseCatalog:
    catalog_id: str
    created_at_utc: str
    entries: List[UniverseCatalogEntry] = field(default_factory=list)
    active_snapshot_id: Optional[str] = None

def build_universe_catalog(data_root: Path) -> UniverseCatalog:
    from usa_signal_bot.universe.sources import default_universe_sources
    from usa_signal_bot.universe.snapshots import list_universe_snapshots, get_latest_active_snapshot

    import uuid

    catalog = UniverseCatalog(
        catalog_id=f"cat_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

    # 1. Add sources (watchlist, presets, imports)
    sources = default_universe_sources(data_root)
    for src in sources:
        # Try to count lines for quick symbol count, rough approx
        count = None
        if src.path:
            p = Path(src.path)
            if p.exists() and p.is_file():
                try:
                    with open(p, 'r', encoding='utf-8') as f:
                        count = sum(1 for _ in f) - 1 # rough approx, ignoring headers
                        count = max(0, count)
                except Exception:
                    pass

        entry = UniverseCatalogEntry(
            entry_id=src.source_id,
            name=src.name,
            layer=src.layer,
            source_type=src.source_type,
            path=str(Path(src.path).relative_to(data_root)) if src.path else "",
            active=src.enabled,
            created_at_utc=src.created_at_utc or catalog.created_at_utc,
            symbol_count=count,
            notes=src.description
        )
        catalog.entries.append(entry)

    # 2. Add snapshots
    snapshots = list_universe_snapshots(data_root)
    active_snap = get_latest_active_snapshot(data_root)

    if active_snap:
        catalog.active_snapshot_id = active_snap.snapshot_id

    for snap in snapshots:
        entry = UniverseCatalogEntry(
            entry_id=snap.snapshot_id,
            name=f"snapshot_{snap.name}",
            layer=UniverseLayer.CANDIDATE, # General layer for snapshots
            source_type=UniverseSourceType.SNAPSHOT,
            path=snap.universe_file,
            active=snap.status == UniverseSnapshotStatus.ACTIVE,
            created_at_utc=snap.created_at_utc,
            symbol_count=snap.symbol_count,
            notes=f"Status: {snap.status.value if hasattr(snap.status, 'value') else str(snap.status)}"
        )
        catalog.entries.append(entry)

    return catalog

def write_universe_catalog(data_root: Path, catalog: UniverseCatalog) -> Path:
    import json

    catalog_dir = data_root / "universe" / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)

    path = catalog_dir / "catalog.json"

    import tempfile
    import os
    fd, temp_path_str = tempfile.mkstemp(dir=str(catalog_dir), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        with open(fd, "w", encoding="utf-8") as f:
            json.dump(catalog_to_dict(catalog), f, indent=2)
        os.replace(temp_path, path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise

    return path

def read_universe_catalog(data_root: Path) -> Optional[UniverseCatalog]:
    path = data_root / "universe" / "catalog" / "catalog.json"
    if not path.exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        catalog = UniverseCatalog(
            catalog_id=data["catalog_id"],
            created_at_utc=data["created_at_utc"],
            active_snapshot_id=data.get("active_snapshot_id")
        )

        for e_data in data.get("entries", []):
            catalog.entries.append(
                UniverseCatalogEntry(
                    entry_id=e_data["entry_id"],
                    name=e_data["name"],
                    layer=UniverseLayer(e_data["layer"]),
                    source_type=UniverseSourceType(e_data["source_type"]),
                    path=e_data["path"],
                    active=e_data["active"],
                    created_at_utc=e_data["created_at_utc"],
                    symbol_count=e_data.get("symbol_count"),
                    notes=e_data.get("notes")
                )
            )

        return catalog
    except Exception as e:
        raise UniverseCatalogError(f"Failed to read catalog: {e}")

def list_catalog_entries(catalog: UniverseCatalog) -> List[UniverseCatalogEntry]:
    return catalog.entries

def catalog_to_text(catalog: UniverseCatalog) -> str:
    lines = [
        "--- Universe Catalog ---",
        f"Catalog ID        : {catalog.catalog_id}",
        f"Created At        : {catalog.created_at_utc}",
        f"Active Snapshot ID: {catalog.active_snapshot_id or 'None'}",
        "\nEntries:"
    ]

    for entry in catalog.entries:
        lines.append(f"  - [{entry.layer.value if hasattr(entry.layer, 'value') else str(entry.layer)}] {entry.name}")
        lines.append(f"      Type   : {entry.source_type.value if hasattr(entry.source_type, 'value') else str(entry.source_type)}")
        lines.append(f"      Active : {'Yes' if entry.active else 'No'}")
        if entry.symbol_count is not None:
             lines.append(f"      Symbols: {entry.symbol_count}")
        lines.append(f"      Path   : {entry.path}")
        if entry.notes:
            lines.append(f"      Notes  : {entry.notes}")
        lines.append("")

    return "\n".join(lines)

def catalog_to_dict(catalog: UniverseCatalog) -> dict:
    return {
        "catalog_id": catalog.catalog_id,
        "created_at_utc": catalog.created_at_utc,
        "active_snapshot_id": catalog.active_snapshot_id,
        "entries": [
            {
                "entry_id": e.entry_id,
                "name": e.name,
                "layer": e.layer.value if hasattr(e.layer, 'value') else str(e.layer),
                "source_type": e.source_type.value if hasattr(e.source_type, 'value') else str(e.source_type),
                "path": e.path,
                "active": e.active,
                "created_at_utc": e.created_at_utc,
                "symbol_count": e.symbol_count,
                "notes": e.notes
            } for e in catalog.entries
        ]
    }
