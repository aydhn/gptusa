import pytest
from pathlib import Path
from usa_signal_bot.universe_lifecycle.lifecycle_store import (
    write_lifecycle_records_jsonl, write_symbol_aliases_jsonl,
    write_universe_snapshot_json, write_symbol_history_checks_jsonl,
    write_survivorship_assessment_json, write_universe_lifecycle_review_json,
    read_universe_snapshot_json, read_universe_lifecycle_review_json,
    list_universe_lifecycle_reviews, get_latest_universe_lifecycle_review,
    lifecycle_store_summary
)
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    SymbolLifecycleRecord, SymbolAliasRecord, UniverseSnapshot,
    SymbolHistoryCheck, SurvivorshipBiasAssessment, UniverseLifecycleReviewResult
)
from usa_signal_bot.core.enums import (
    SymbolLifecycleStatus, SymbolLifecycleSource, SymbolAliasType,
    UniverseSnapshotType, SymbolHistoryStatus, SurvivorshipBiasRisk,
    UniverseGuardStatus, UniverseLifecycleReportType
)

def test_write_lifecycle_records_jsonl(tmp_path):
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    p = tmp_path / "records.jsonl"
    write_lifecycle_records_jsonl(p, [r1])
    assert p.exists()

def test_write_symbol_aliases_jsonl(tmp_path):
    a1 = SymbolAliasRecord("id", "FB", "META", SymbolAliasType.TICKER_CHANGE)
    p = tmp_path / "aliases.jsonl"
    write_symbol_aliases_jsonl(p, [a1])
    assert p.exists()

def test_write_universe_snapshot_json(tmp_path):
    s = UniverseSnapshot("id", "now", UniverseSnapshotType.CURRENT, "now", "u1", ["AAPL"], SymbolLifecycleSource.MANUAL_REGISTRY, 1)
    p = tmp_path / "snap.json"
    write_universe_snapshot_json(p, s)
    assert p.exists()

    loaded = read_universe_snapshot_json(p)
    assert loaded["symbols"] == ["AAPL"]

def test_write_symbol_history_checks_jsonl(tmp_path):
    c1 = SymbolHistoryCheck("1", "AAPL", "now", SymbolHistoryStatus.SUFFICIENT, 100)
    p = tmp_path / "checks.jsonl"
    write_symbol_history_checks_jsonl(p, [c1])
    assert p.exists()

def test_write_survivorship_assessment_json(tmp_path):
    a = SurvivorshipBiasAssessment("id", "now", "u", "now", UniverseGuardStatus.CLEAR, SurvivorshipBiasRisk.LOW, 1)
    p = tmp_path / "assess.json"
    write_survivorship_assessment_json(p, a)
    assert p.exists()

def test_write_universe_lifecycle_review_json(tmp_path):
    s = UniverseSnapshot("id", "now", UniverseSnapshotType.CURRENT, "now", "u1", ["AAPL"], SymbolLifecycleSource.MANUAL_REGISTRY, 1)
    rev = UniverseLifecycleReviewResult("id", "now", UniverseLifecycleReportType.FULL_UNIVERSE_LIFECYCLE_REVIEW, "u", [], [], [s], [], None)

    p = tmp_path / "universe_lifecycle" / "reviews" / "rev.json"
    write_universe_lifecycle_review_json(p, rev)
    assert p.exists()

    loaded = read_universe_lifecycle_review_json(p)
    assert loaded["universe_name"] == "u"

    res = list_universe_lifecycle_reviews(tmp_path)
    assert len(res) == 1

    latest = get_latest_universe_lifecycle_review(tmp_path)
    assert latest == p

def test_lifecycle_store_summary(tmp_path):
    summ = lifecycle_store_summary(tmp_path)
    assert summ["reviews"] == 0
