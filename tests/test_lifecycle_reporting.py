import pytest
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolLifecycleRecord, SymbolAliasRecord, UniverseSnapshot,
    SurvivorshipBiasAssessment, UniverseLifecycleReviewResult
)
from usa_signal_bot.core.enums import (
    SymbolLifecycleStatus, SymbolLifecycleSource, SymbolAliasType,
    UniverseSnapshotType, SurvivorshipBiasRisk, UniverseGuardStatus,
    UniverseLifecycleReportType
)
from usa_signal_bot.universe_lifecycle.lifecycle_reporting import (
    symbol_lifecycle_record_to_text, symbol_alias_record_to_text,
    survivorship_bias_assessment_to_text, universe_lifecycle_review_result_to_text,
    lifecycle_store_summary_to_text, lifecycle_limitations_text
)

def test_symbol_lifecycle_record_to_text():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    text = symbol_lifecycle_record_to_text(r1)
    assert "AAPL" in text
    assert "ACTIVE" in text
    assert "MANUAL_REGISTRY" in text

def test_symbol_alias_record_to_text():
    a1 = SymbolAliasRecord("id", "FB", "META", SymbolAliasType.TICKER_CHANGE)
    text = symbol_alias_record_to_text(a1)
    assert "FB" in text
    assert "META" in text
    assert "TICKER_CHANGE" in text

def test_survivorship_bias_assessment_to_text():
    a = SurvivorshipBiasAssessment("id", "now", "u", "now", UniverseGuardStatus.WARNING, SurvivorshipBiasRisk.HIGH, 10, delisted_symbol_count=2, warnings=["Test warning"])
    text = survivorship_bias_assessment_to_text(a)
    assert "Survivorship Bias Assessment" in text
    assert "HIGH" in text
    assert "Test warning" in text

def test_universe_lifecycle_review_result_to_text():
    rev = UniverseLifecycleReviewResult("id", "now", UniverseLifecycleReportType.FULL_UNIVERSE_LIFECYCLE_REVIEW, "u", [], [], [], [], None)
    text = universe_lifecycle_review_result_to_text(rev)
    assert "Universe Lifecycle Review: u" in text

def test_lifecycle_limitations_text():
    text = lifecycle_limitations_text()
    assert "LIMITATIONS" in text
    assert "investment advice" in text
    assert "live trading" in text
