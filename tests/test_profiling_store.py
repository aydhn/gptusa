import pytest
from pathlib import Path
from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceProfile
from usa_signal_bot.profiling.profiling_store import write_resource_profile_json, list_resource_profiles, profiling_store_summary

def test_profiling_store(tmp_path):
    prof = ResourceProfile("res_profile_1", ResourceProfileScope.TASK, "t", ResourceProfileStatus.COMPLETED, None, None, 1.0, 0, 0, 0, 0, 0, 0, 0, [], [], [])

    file_path = tmp_path / "profiling" / "profiles" / "res_profile_1.json"
    write_resource_profile_json(file_path, prof)

    files = list_resource_profiles(tmp_path)
    assert len(files) == 1

    summary = profiling_store_summary(tmp_path)
    assert summary["profile_count"] == 1
