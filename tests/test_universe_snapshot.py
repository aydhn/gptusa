import pytest
from pathlib import Path
from usa_signal_bot.universe_lifecycle.universe_snapshot import (
    build_universe_snapshot, compare_universe_snapshots, symbols_added_between_snapshots,
    symbols_removed_between_snapshots, universe_snapshot_to_text
)
from usa_signal_bot.core.enums import UniverseSnapshotType, SymbolLifecycleSource

def test_build_universe_snapshot():
    s = build_universe_snapshot("my_univ", ["aapl", "msft", "aapl"], UniverseSnapshotType.CURRENT)
    assert s.symbol_count == 2
    assert "AAPL" in s.symbols
    assert "MSFT" in s.symbols

def test_compare_universe_snapshots():
    s1 = build_universe_snapshot("my_univ", ["AAPL", "MSFT"], UniverseSnapshotType.HISTORICAL)
    s2 = build_universe_snapshot("my_univ", ["AAPL", "TSLA"], UniverseSnapshotType.CURRENT)

    added = symbols_added_between_snapshots(s1, s2)
    removed = symbols_removed_between_snapshots(s1, s2)
    assert added == ["TSLA"]
    assert removed == ["MSFT"]

    diff = compare_universe_snapshots(s1, s2)
    assert diff["added_count"] == 1
    assert diff["removed_count"] == 1

def test_snapshot_text():
    s = build_universe_snapshot("my_univ", ["AAPL"], UniverseSnapshotType.CURRENT)
    text = universe_snapshot_to_text(s)
    assert "Universe Snapshot" in text
    assert "AAPL" not in text # Text format doesn't print symbols directly, just counts
    assert "Symbol Count: 1" in text
