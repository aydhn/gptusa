import pytest
from usa_signal_bot.core.enums import BaselineStatus, PerformanceBaselineScope
from usa_signal_bot.performance.baseline_models import PerformanceBaseline
from usa_signal_bot.performance.baseline_versioning import (
    create_baseline_version, parse_baseline_version, supersede_baseline, mark_baseline_stale, baseline_version_to_text
)

def test_create_baseline_version():
    v = create_baseline_version()
    assert v.startswith("baseline_v_")

def test_parse_baseline_version():
    v = create_baseline_version("test")
    p = parse_baseline_version(v)
    assert p["prefix"] == "test"
    assert p["parsed_timestamp"] is not None

def test_supersede_baseline():
    b1 = PerformanceBaseline("b1", "v1", PerformanceBaselineScope.SCAN, BaselineStatus.ACTIVE, "", 0, [], [], [], [], {})
    b2 = PerformanceBaseline("b2", "v2", PerformanceBaselineScope.SCAN, BaselineStatus.ACTIVE, "", 0, [], [], [], [], {})
    res = supersede_baseline(b1, b2)
    assert res.status == BaselineStatus.SUPERSEDED
    assert res.metadata["superseded_by"] == "b2"

def test_mark_baseline_stale():
    b1 = PerformanceBaseline("b1", "v1", PerformanceBaselineScope.SCAN, BaselineStatus.ACTIVE, "", 0, [], [], [], [], {})
    res = mark_baseline_stale(b1, "too old")
    assert res.status == BaselineStatus.STALE
    assert res.metadata["stale_reason"] == "too old"

def test_baseline_version_to_text():
    v = create_baseline_version()
    txt = baseline_version_to_text(v)
    assert "Version: " in txt
