import pytest
from pathlib import Path
from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus
from usa_signal_bot.profiling.resource_profile_collector import ResourceProfileCollector

def test_profile_noop(tmp_path):
    collector = ResourceProfileCollector(tmp_path)
    profile = collector.profile_noop(ResourceProfileScope.TASK)

    assert profile.status == ResourceProfileStatus.COMPLETED
    assert profile.wall_time_seconds > 0
    assert profile.target_name == "noop"

def test_profile_artifact_path(tmp_path):
    (tmp_path / "file1.txt").write_text("hello")
    collector = ResourceProfileCollector(tmp_path)
    profile = collector.profile_artifact_path(tmp_path, ResourceProfileScope.CUSTOM, "test_target")
    assert profile.status == ResourceProfileStatus.COMPLETED
    assert profile.artifact_size_bytes == 5
    assert profile.artifact_file_count == 1

def test_collect_lightweight_snapshot(tmp_path):
    collector = ResourceProfileCollector(tmp_path)
    profiles = collector.collect_lightweight_snapshot()
    assert len(profiles) >= 1
    assert any(p.target_name == "noop" for p in profiles)
