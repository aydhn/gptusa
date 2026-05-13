import pytest
from usa_signal_bot.universe_lifecycle.delisting_awareness import check_symbol_delisting_awareness, infer_delisting_risk_from_history
from usa_signal_bot.universe_lifecycle.symbol_status_resolver import SymbolStatusResolver
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolLifecycleRecord, SymbolHistoryCheck
from usa_signal_bot.core.enums import SymbolLifecycleStatus, SymbolLifecycleSource, SurvivorshipBiasRisk, SymbolHistoryStatus

def test_check_symbol_delisting_awareness():
    r1 = SymbolLifecycleRecord("TWTR", SymbolLifecycleStatus.DELISTED, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])

    res = check_symbol_delisting_awareness("TWTR", resolver)
    assert res.status == SymbolLifecycleStatus.DELISTED
    assert res.risk == SurvivorshipBiasRisk.CRITICAL

def test_infer_delisting_risk_from_history():
    c = SymbolHistoryCheck("id", "AAPL", "now", SymbolHistoryStatus.SUFFICIENT, 500)
    assert infer_delisting_risk_from_history(c) == SurvivorshipBiasRisk.LOW

    c.status = SymbolHistoryStatus.STALE_HISTORY
    assert infer_delisting_risk_from_history(c) == SurvivorshipBiasRisk.HIGH

def test_check_symbol_delisting_awareness_with_history():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])

    c = SymbolHistoryCheck("id", "AAPL", "now", SymbolHistoryStatus.STALE_HISTORY, 500)

    res = check_symbol_delisting_awareness("AAPL", resolver, history_check=c)
    assert res.risk == SurvivorshipBiasRisk.MODERATE
    assert len(res.warnings) > 0
