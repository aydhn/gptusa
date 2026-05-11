import pytest
from pathlib import Path
from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceProfile
from usa_signal_bot.profiling.profiling_store import write_resource_profile_json
from usa_signal_bot.profiling.run_metrics_loader import load_profiles_from_store, extract_duration_values, summarize_historical_metrics

def test_load_profiles_from_store(tmp_path):
    prof1 = ResourceProfile("p1", ResourceProfileScope.TASK, "t1", ResourceProfileStatus.COMPLETED, "2023-01-01T00:00:00Z", "2023-01-01T00:00:01Z", 1.0, 0.5, None, None, None, None, None, None, [], [], [])
    prof2 = ResourceProfile("p2", ResourceProfileScope.SCAN, "t2", ResourceProfileStatus.COMPLETED, "2023-01-02T00:00:00Z", "2023-01-02T00:00:01Z", 2.0, 1.0, None, None, None, None, None, None, [], [], [])

    write_resource_profile_json(tmp_path / "profiling" / "profiles" / "res_profile_1.json", prof1)
    write_resource_profile_json(tmp_path / "profiling" / "profiles" / "res_profile_2.json", prof2)

    profiles = load_profiles_from_store(tmp_path)
    assert len(profiles) == 2

    scan_profiles = load_profiles_from_store(tmp_path, scope=ResourceProfileScope.SCAN)
    assert len(scan_profiles) == 1
    assert scan_profiles[0].profile_id == "p2"

def test_extract_duration_values():
    records = [{"duration_seconds": 1.5}, {"duration_seconds": 2.5}, {"other": 3.0}]
    vals = extract_duration_values(records)
    assert vals == [1.5, 2.5]

def test_summarize_historical_metrics():
    summary = summarize_historical_metrics([{}, {}])
    assert summary["count"] == 2
