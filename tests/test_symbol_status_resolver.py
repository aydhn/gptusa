import pytest
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolLifecycleRecord, SymbolAliasRecord
from usa_signal_bot.core.enums import SymbolLifecycleStatus, SymbolLifecycleSource, SymbolAliasType
from usa_signal_bot.universe_lifecycle.symbol_status_resolver import SymbolStatusResolver

def test_resolve_status_active():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    res = SymbolStatusResolver([r1]).resolve_status("AAPL")
    assert res.status == SymbolLifecycleStatus.ACTIVE

def test_resolve_status_unknown():
    res = SymbolStatusResolver([]).resolve_status("AAPL")
    assert res.status == SymbolLifecycleStatus.UNKNOWN

def test_resolve_status_with_as_of_date():
    r1 = SymbolLifecycleRecord("TWTR", SymbolLifecycleStatus.DELISTED, SymbolLifecycleSource.MANUAL_REGISTRY, delisted_date="2022-10-28")

    resolver = SymbolStatusResolver([r1])
    # Before delisting
    res_before = resolver.resolve_status("TWTR", as_of_date="2022-10-27")
    assert res_before.status == SymbolLifecycleStatus.ACTIVE

    # After delisting
    res_after = resolver.resolve_status("TWTR", as_of_date="2022-10-29")
    assert res_after.status == SymbolLifecycleStatus.DELISTED

def test_resolve_successor():
    a1 = SymbolAliasRecord("id", "FB", "META", SymbolAliasType.TICKER_CHANGE)
    resolver = SymbolStatusResolver(aliases=[a1])

    assert resolver.resolve_successor("FB") == "META"
    assert resolver.resolve_predecessor("META") == "FB"

def test_requires_review():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.REVIEW_REQUIRED, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])
    assert resolver.requires_review("AAPL") is True
    assert resolver.requires_review("MSFT") is True # Unknown also requires review
