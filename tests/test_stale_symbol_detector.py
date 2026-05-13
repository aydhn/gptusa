import pytest
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolHistoryCheck, SymbolLifecycleRecord
from usa_signal_bot.core.enums import SymbolHistoryStatus, SymbolLifecycleStatus, SymbolLifecycleSource
from usa_signal_bot.universe_lifecycle.stale_symbol_detector import (
    detect_stale_symbols, detect_symbols_with_missing_history, detect_symbols_requiring_review, stale_symbol_summary
)

def test_detect_stale_symbols():
    c1 = SymbolHistoryCheck("1", "AAPL", "now", SymbolHistoryStatus.STALE_HISTORY, 100, stale_days=20)
    c2 = SymbolHistoryCheck("2", "MSFT", "now", SymbolHistoryStatus.SUFFICIENT, 100, stale_days=0)

    res = detect_stale_symbols([c1, c2])
    assert len(res) == 1
    assert res[0].symbol == "AAPL"

def test_detect_missing_history():
    c1 = SymbolHistoryCheck("1", "AAPL", "now", SymbolHistoryStatus.MISSING_HISTORY, 0)
    res = detect_symbols_with_missing_history([c1])
    assert len(res) == 1

def test_detect_symbols_requiring_review():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    r2 = SymbolLifecycleRecord("MSFT", SymbolLifecycleStatus.UNKNOWN, SymbolLifecycleSource.MANUAL_REGISTRY)

    c1 = SymbolHistoryCheck("1", "AAPL", "now", SymbolHistoryStatus.STALE_HISTORY, 100)

    # AAPL is ACTIVE but stale -> needs review
    # MSFT is UNKNOWN -> needs review
    res = detect_symbols_requiring_review([r1, r2], [c1])
    assert sorted(res) == ["AAPL", "MSFT"]

def test_stale_symbol_summary():
    c1 = SymbolHistoryCheck("1", "AAPL", "now", SymbolHistoryStatus.STALE_HISTORY, 100)
    summ = stale_symbol_summary([c1])
    assert summ["stale_count"] == 1
    assert summ["stale_symbols"] == ["AAPL"]
