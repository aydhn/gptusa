import pytest
from usa_signal_bot.universe_lifecycle.survivorship_bias_guard import SurvivorshipBiasGuard
from usa_signal_bot.universe_lifecycle.symbol_status_resolver import SymbolStatusResolver
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolLifecycleRecord, UniverseSnapshot
from usa_signal_bot.core.enums import SymbolLifecycleStatus, SymbolLifecycleSource, SurvivorshipBiasRisk, UniverseGuardStatus, UniverseSnapshotType

def test_assess_universe_full_coverage():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])
    guard = SurvivorshipBiasGuard(resolver)

    res = guard.assess_universe(["AAPL"], "test")
    assert res.risk == SurvivorshipBiasRisk.LOW
    assert res.status == UniverseGuardStatus.CLEAR

def test_assess_universe_unknown_warning():
    resolver = SymbolStatusResolver([])
    guard = SurvivorshipBiasGuard(resolver)

    res = guard.assess_universe(["AAPL"], "test")
    assert res.risk == SurvivorshipBiasRisk.HIGH # 100% unknown
    assert res.status == UniverseGuardStatus.WARNING

def test_assess_universe_delisted():
    r1 = SymbolLifecycleRecord("TWTR", SymbolLifecycleStatus.DELISTED, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])
    guard = SurvivorshipBiasGuard(resolver)

    res = guard.assess_universe(["TWTR"], "test")
    assert res.risk == SurvivorshipBiasRisk.CRITICAL
    assert res.status == UniverseGuardStatus.BLOCK_BACKTEST

def test_assess_backtest_universe_current_only():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])
    guard = SurvivorshipBiasGuard(resolver, historical_snapshots=[])

    res = guard.assess_backtest_universe(["AAPL"], "test", "2020-01-01T00:00:00Z", "2021-01-01T00:00:00Z")
    assert res.risk == SurvivorshipBiasRisk.HIGH
    assert res.status == UniverseGuardStatus.WARNING
    assert "use_historical_universe_snapshot" in guard.recommended_guards(res)

def test_assess_scan_universe():
    r1 = SymbolLifecycleRecord("TWTR", SymbolLifecycleStatus.DELISTED, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])
    guard = SurvivorshipBiasGuard(resolver)

    res = guard.assess_scan_universe(["TWTR"], "test")
    assert res.risk == SurvivorshipBiasRisk.CRITICAL
    assert res.status == UniverseGuardStatus.BLOCK_BACKTEST
