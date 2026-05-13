import pytest
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolLifecycleRecord
from usa_signal_bot.core.enums import SymbolLifecycleStatus, SymbolLifecycleSource, UniverseSnapshotType
from usa_signal_bot.universe_lifecycle.lifecycle_registry import (
    merge_lifecycle_records, lifecycle_record_for_symbol,
    infer_lifecycle_records_from_snapshots, lifecycle_registry_to_text
)
from usa_signal_bot.universe_lifecycle.universe_snapshot import build_universe_snapshot

def test_merge_lifecycle_records():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    r2 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.UNKNOWN, SymbolLifecycleSource.INFERRED_FROM_HISTORY)
    r3 = SymbolLifecycleRecord("MSFT", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)

    merged = merge_lifecycle_records([r1], [r2, r3])
    assert len(merged) == 2
    aapl_rec = [r for r in merged if r.symbol == "AAPL"][0]
    assert aapl_rec.status == SymbolLifecycleStatus.ACTIVE # r1 overrides r2

def test_lifecycle_record_for_symbol():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    res = lifecycle_record_for_symbol([r1], "aapl")
    assert res == r1

def test_infer_lifecycle_records_from_snapshots():
    s1 = build_universe_snapshot("univ", ["AAPL", "MSFT"], UniverseSnapshotType.HISTORICAL, as_of_date="2020-01-01")
    s2 = build_universe_snapshot("univ", ["AAPL", "TSLA"], UniverseSnapshotType.HISTORICAL, as_of_date="2021-01-01")

    records = infer_lifecycle_records_from_snapshots([s1, s2])
    assert len(records) == 3

    msft = [r for r in records if r.symbol == "MSFT"][0]
    assert msft.status == SymbolLifecycleStatus.INACTIVE

    aapl = [r for r in records if r.symbol == "AAPL"][0]
    assert aapl.status == SymbolLifecycleStatus.ACTIVE

def test_lifecycle_registry_to_text():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    text = lifecycle_registry_to_text([r1])
    assert "AAPL: ACTIVE" in text
