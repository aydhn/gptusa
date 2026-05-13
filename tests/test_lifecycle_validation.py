import pytest
from usa_signal_bot.universe_lifecycle.lifecycle_validation import (
    validate_lifecycle_registry_report, validate_symbol_aliases_report,
    validate_universe_snapshot_report, validate_symbol_history_checks_report,
    validate_survivorship_assessment_report, validate_no_sensitive_data_in_lifecycle_payload,
    validate_no_live_execution_language_in_lifecycle, assert_lifecycle_valid
)
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolLifecycleRecord, SymbolAliasRecord, UniverseSnapshot,
    SymbolHistoryCheck, SurvivorshipBiasAssessment
)
from usa_signal_bot.core.enums import (
    SymbolLifecycleStatus, SymbolLifecycleSource, SymbolAliasType,
    UniverseSnapshotType, SymbolHistoryStatus, SurvivorshipBiasRisk,
    UniverseGuardStatus
)
from usa_signal_bot.core.exceptions import LifecycleValidationError

def test_validate_registry_valid():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    rep = validate_lifecycle_registry_report([r1])
    assert rep.valid is True

def test_validate_registry_invalid_date():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.DELISTED, SymbolLifecycleSource.MANUAL_REGISTRY,
                              listed_date="2022-01-01", delisted_date="2020-01-01")
    rep = validate_lifecycle_registry_report([r1])
    assert rep.valid is False
    assert rep.error_count == 1

def test_validate_aliases_cycle_self():
    a1 = SymbolAliasRecord("id", "FB", "FB", SymbolAliasType.TICKER_CHANGE)
    rep = validate_symbol_aliases_report([a1])
    assert rep.valid is False

def test_validate_snapshot_count_mismatch():
    s = UniverseSnapshot("id", "now", UniverseSnapshotType.CURRENT, "now", "u1", ["AAPL", "MSFT"], SymbolLifecycleSource.MANUAL_REGISTRY, 1)
    rep = validate_universe_snapshot_report(s)
    assert rep.valid is False

def test_validate_assessment_bad_count():
    a = SurvivorshipBiasAssessment("id", "now", "u", "now", UniverseGuardStatus.CLEAR, SurvivorshipBiasRisk.LOW, current_symbol_count=5, delisted_symbol_count=10)
    rep = validate_survivorship_assessment_report(a)
    assert rep.valid is False

def test_no_sensitive_data():
    payload = {"status": "ACTIVE", "api_key": "12345"}
    rep = validate_no_sensitive_data_in_lifecycle_payload(payload)
    assert rep.valid is False

def test_no_live_execution_language():
    rep = validate_no_live_execution_language_in_lifecycle("This is live approved to run")
    assert rep.valid is False

    rep2 = validate_no_live_execution_language_in_lifecycle("Just a dry run review")
    assert rep2.valid is True

def test_assert_lifecycle_valid():
    rep = validate_no_live_execution_language_in_lifecycle("This is live approved to run")
    with pytest.raises(LifecycleValidationError):
        assert_lifecycle_valid(rep)
