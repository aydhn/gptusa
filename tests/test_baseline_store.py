import pytest
from pathlib import Path
from usa_signal_bot.core.enums import PerformanceBaselineScope, BaselineStatus
from usa_signal_bot.performance.baseline_models import PerformanceBaseline
from usa_signal_bot.performance.baseline_store import (
    baseline_store_dir, baselines_dir, write_performance_baseline_json, list_performance_baselines, baseline_store_summary
)

def test_dirs(tmp_path):
    assert baseline_store_dir(tmp_path).name == "performance"
    assert baselines_dir(tmp_path).name == "baselines"

def test_write_and_list_baselines(tmp_path):
    b = PerformanceBaseline("b1", "v1", PerformanceBaselineScope.SCAN, BaselineStatus.ACTIVE, "", 0, [], [], [], [], {})
    write_performance_baseline_json(tmp_path / "performance" / "baselines" / "b1.json", b)

    lst = list_performance_baselines(tmp_path)
    assert len(lst) == 1
    assert lst[0].name == "b1.json"

def test_baseline_store_summary(tmp_path):
    b = PerformanceBaseline("b1", "v1", PerformanceBaselineScope.SCAN, BaselineStatus.ACTIVE, "", 0, [], [], [], [], {})
    write_performance_baseline_json(tmp_path / "performance" / "baselines" / "b1.json", b)

    sum = baseline_store_summary(tmp_path)
    assert sum["baseline_count"] == 1
