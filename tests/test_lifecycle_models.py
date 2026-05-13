import pytest
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolLifecycleRecord, SymbolAliasRecord, UniverseSnapshot,
    SymbolHistoryCheck, SurvivorshipBiasAssessment, UniverseLifecycleReviewResult,
    validate_symbol_lifecycle_record, validate_universe_snapshot, create_universe_snapshot_id
)
from usa_signal_bot.core.enums import SymbolLifecycleStatus, SymbolLifecycleSource, UniverseSnapshotType, SymbolAliasType, SymbolHistoryStatus, SurvivorshipBiasRisk, UniverseGuardStatus, UniverseLifecycleReportType
from usa_signal_bot.core.exceptions import LifecycleValidationError

def test_symbol_lifecycle_record_valid():
    r = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    validate_symbol_lifecycle_record(r)
    assert r.symbol == "AAPL"

def test_symbol_lifecycle_record_invalid_dates():
    r = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.DELISTED, SymbolLifecycleSource.MANUAL_REGISTRY,
                              listed_date="2022-01-01", delisted_date="2020-01-01")
    with pytest.raises(LifecycleValidationError):
        validate_symbol_lifecycle_record(r)

def test_symbol_alias_record():
    a = SymbolAliasRecord("a1", "FB", "META", SymbolAliasType.TICKER_CHANGE)
    assert a.old_symbol == "FB"
    assert a.new_symbol == "META"

def test_universe_snapshot_valid():
    s = UniverseSnapshot("s1", "2022-01-01", UniverseSnapshotType.CURRENT, "2022-01-01", "my_univ", ["AAPL"], SymbolLifecycleSource.MANUAL_REGISTRY, 1)
    validate_universe_snapshot(s)

def test_universe_snapshot_invalid_count():
    s = UniverseSnapshot("s1", "2022-01-01", UniverseSnapshotType.CURRENT, "2022-01-01", "my_univ", ["AAPL"], SymbolLifecycleSource.MANUAL_REGISTRY, 2)
    with pytest.raises(LifecycleValidationError):
        validate_universe_snapshot(s)
