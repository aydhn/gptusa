import pytest
from usa_signal_bot.universe.snapshots import (
    write_universe_snapshot,
    read_universe_snapshot,
    mark_snapshot_active,
    get_latest_active_snapshot,
    archive_snapshot
)
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol
from usa_signal_bot.core.enums import UniverseSnapshotStatus

def test_write_and_read_snapshot(tmp_path):
    univ = UniverseDefinition(name="test", symbols=[UniverseSymbol(symbol="AAPL")])
    snap = write_universe_snapshot(tmp_path, univ)

    assert snap.status == UniverseSnapshotStatus.DRAFT
    assert snap.symbol_count == 1

    read_snap = read_universe_snapshot(tmp_path / "universe" / "snapshots" / f"{snap.snapshot_id}_meta.json")
    assert read_snap.snapshot_id == snap.snapshot_id
    assert read_snap.symbol_count == 1

def test_active_snapshot(tmp_path):
    univ = UniverseDefinition(name="test", symbols=[UniverseSymbol(symbol="AAPL")])
    snap = write_universe_snapshot(tmp_path, univ)

    mark_snapshot_active(tmp_path, snap.snapshot_id)

    active = get_latest_active_snapshot(tmp_path)
    assert active is not None
    assert active.snapshot_id == snap.snapshot_id
    assert active.status == UniverseSnapshotStatus.ACTIVE

def test_archive_snapshot(tmp_path):
    univ = UniverseDefinition(name="test", symbols=[UniverseSymbol(symbol="AAPL")])
    snap = write_universe_snapshot(tmp_path, univ)

    archive_snapshot(tmp_path, snap.snapshot_id)

    read_snap = read_universe_snapshot(tmp_path / "universe" / "snapshots" / f"{snap.snapshot_id}_meta.json")
    assert read_snap.status == UniverseSnapshotStatus.ARCHIVED
