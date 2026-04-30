import pytest
from pathlib import Path
from usa_signal_bot.core.enums import UniverseSourceType, UniverseLayer
from usa_signal_bot.universe.sources import (
    UniverseSource,
    create_universe_source,
    validate_universe_source,
    source_to_dict,
    default_universe_sources
)
from usa_signal_bot.core.exceptions import UniverseSourceError

def test_create_universe_source():
    src = create_universe_source("test", UniverseSourceType.MANUAL_SEED, None, UniverseLayer.CORE)
    assert src.name == "test"
    assert src.source_type == UniverseSourceType.MANUAL_SEED
    assert src.layer == UniverseLayer.CORE
    assert src.enabled is True
    assert src.source_id.startswith("test_")

def test_validate_universe_source_missing_path():
    with pytest.raises(UniverseSourceError) as e:
        create_universe_source("test", UniverseSourceType.USER_CSV, None, UniverseLayer.CORE)
    assert "path cannot be empty" in str(e.value)

def test_validate_universe_source_reserved_external():
    with pytest.raises(UniverseSourceError) as e:
        src = UniverseSource(
            source_id="id",
            name="test",
            source_type=UniverseSourceType.RESERVED_EXTERNAL,
            layer=UniverseLayer.CORE,
            enabled=True
        )
        validate_universe_source(src)
    assert "RESERVED_EXTERNAL source type cannot be enabled" in str(e.value)

def test_source_to_dict():
    src = create_universe_source("test", UniverseSourceType.MANUAL_SEED, None, UniverseLayer.CORE)
    d = source_to_dict(src)
    assert d["name"] == "test"
    assert d["source_type"] == "MANUAL_SEED"
    assert d["layer"] == "CORE"

def test_default_universe_sources(tmp_path):
    # Setup mock structure
    (tmp_path / "universe" / "presets").mkdir(parents=True)
    (tmp_path / "universe" / "imports").mkdir(parents=True)

    (tmp_path / "universe" / "presets" / "core_watchlist.csv").touch()

    sources = default_universe_sources(tmp_path)
    assert len(sources) >= 2 # Watchlist + core preset
    names = [s.name for s in sources]
    assert "default_watchlist" in names
    assert "preset_core_watchlist" in names
