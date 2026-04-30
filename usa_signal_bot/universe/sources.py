from dataclasses import dataclass, field
from typing import Any, List, Optional
from pathlib import Path

from usa_signal_bot.core.enums import UniverseSourceType, UniverseLayer
from usa_signal_bot.universe.models import UniverseDefinition
from usa_signal_bot.core.exceptions import UniverseSourceError

@dataclass
class UniverseSource:
    source_id: str
    name: str
    source_type: UniverseSourceType
    layer: UniverseLayer
    path: Optional[str] = None
    enabled: bool = True
    priority: int = 100
    description: Optional[str] = None
    created_at_utc: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class UniverseSourceLoadResult:
    source: UniverseSource
    universe: Optional[UniverseDefinition]
    success: bool
    symbol_count: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_universe_source(
    name: str,
    source_type: UniverseSourceType,
    path: Optional[str],
    layer: UniverseLayer,
    priority: int = 100
) -> UniverseSource:
    import uuid
    source_id = f"{name}_{uuid.uuid4().hex[:8]}"
    source = UniverseSource(
        source_id=source_id,
        name=name,
        source_type=source_type,
        path=path,
        layer=layer,
        priority=priority
    )
    validate_universe_source(source)
    return source

def validate_universe_source(source: UniverseSource) -> None:
    if not source.source_id:
        raise UniverseSourceError("source_id cannot be empty")
    if not source.name:
        raise UniverseSourceError("name cannot be empty")

    if not isinstance(source.source_type, UniverseSourceType):
        try:
            source.source_type = UniverseSourceType(source.source_type)
        except ValueError:
            raise UniverseSourceError(f"Invalid source_type: {source.source_type}")

    if not isinstance(source.layer, UniverseLayer):
        try:
            source.layer = UniverseLayer(source.layer)
        except ValueError:
            raise UniverseSourceError(f"Invalid layer: {source.layer}")

    if source.priority < 0:
        raise UniverseSourceError("priority cannot be negative")

    path_required_types = [
        UniverseSourceType.USER_CSV,
        UniverseSourceType.LOCAL_IMPORT,
        UniverseSourceType.PRESET,
        UniverseSourceType.SNAPSHOT
    ]
    if source.source_type in path_required_types and not source.path:
        raise UniverseSourceError(f"path cannot be empty for source type {source.source_type}")

    if source.source_type == UniverseSourceType.RESERVED_EXTERNAL and source.enabled:
        raise UniverseSourceError("RESERVED_EXTERNAL source type cannot be enabled in this phase")

def source_to_dict(source: UniverseSource) -> dict:
    return {
        "source_id": source.source_id,
        "name": source.name,
        "source_type": source.source_type.value if hasattr(source.source_type, 'value') else str(source.source_type),
        "path": source.path,
        "layer": source.layer.value if hasattr(source.layer, 'value') else str(source.layer),
        "enabled": source.enabled,
        "priority": source.priority,
        "description": source.description,
        "created_at_utc": source.created_at_utc,
        "metadata": source.metadata
    }

def default_universe_sources(data_root: Path) -> List[UniverseSource]:
    sources = []

    # default watchlist
    sources.append(
        create_universe_source(
            name="default_watchlist",
            source_type=UniverseSourceType.USER_CSV,
            path=str(data_root / "universe" / "watchlist.csv"),
            layer=UniverseLayer.WATCHLIST,
            priority=10
        )
    )

    # presets
    presets_dir = data_root / "universe" / "presets"

    core_watchlist = presets_dir / "core_watchlist.csv"
    if core_watchlist.exists():
        sources.append(
            create_universe_source(
                name="preset_core_watchlist",
                source_type=UniverseSourceType.PRESET,
                path=str(core_watchlist),
                layer=UniverseLayer.CORE,
                priority=20
            )
        )

    mega_cap = presets_dir / "mega_cap_sample.csv"
    if mega_cap.exists():
        sources.append(
            create_universe_source(
                name="preset_mega_cap",
                source_type=UniverseSourceType.PRESET,
                path=str(mega_cap),
                layer=UniverseLayer.MEGA_CAP,
                priority=30
            )
        )

    sector_etf = presets_dir / "sector_etf_sample.csv"
    if sector_etf.exists():
        sources.append(
            create_universe_source(
                name="preset_sector_etf",
                source_type=UniverseSourceType.PRESET,
                path=str(sector_etf),
                layer=UniverseLayer.SECTOR_ETF,
                priority=40
            )
        )

    index_etf = presets_dir / "index_etf_sample.csv"
    if index_etf.exists():
        sources.append(
            create_universe_source(
                name="preset_index_etf",
                source_type=UniverseSourceType.PRESET,
                path=str(index_etf),
                layer=UniverseLayer.INDEX_ETF,
                priority=50
            )
        )

    # imports
    imports_dir = data_root / "universe" / "imports"
    if imports_dir.exists() and imports_dir.is_dir():
        for csv_file in imports_dir.glob("*.csv"):
            sources.append(
                create_universe_source(
                    name=f"import_{csv_file.stem}",
                    source_type=UniverseSourceType.LOCAL_IMPORT,
                    path=str(csv_file),
                    layer=UniverseLayer.CUSTOM,
                    priority=100
                )
            )

    return sources
