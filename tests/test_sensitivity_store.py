import pytest
from pathlib import Path
from usa_signal_bot.core.enums import ParameterGridType, SensitivityRunStatus, StabilityBucket, OverfitRiskHint, SensitivityMetricName
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterGridSpec, ParameterSensitivityConfig, ParameterSensitivityRunResult
)
from usa_signal_bot.backtesting.sensitivity_metrics import SensitivityAggregateMetrics
from usa_signal_bot.backtesting.stability_map import StabilityMap
from usa_signal_bot.backtesting.sensitivity_store import (
    sensitivity_store_dir, build_sensitivity_run_dir,
    write_sensitivity_result_json, write_sensitivity_grid_json,
    write_sensitivity_aggregate_metrics_json, write_stability_map_json,
    list_sensitivity_runs, get_latest_sensitivity_run_dir
)

def test_store_dir_creation(tmp_path: Path):
    d = sensitivity_store_dir(tmp_path)
    assert d.exists()
    assert d.is_dir()
    assert d.name == "sensitivity"

def test_build_sensitivity_run_dir(tmp_path: Path):
    d = build_sensitivity_run_dir(tmp_path, "run_123")
    assert d.exists()
    assert d.name == "run_123"

def test_write_files(tmp_path: Path):
    d = build_sensitivity_run_dir(tmp_path, "run_write")

    grid = ParameterGridSpec("g1", "strat", ParameterGridType.SINGLE_PARAMETER, [], 10)
    config = ParameterSensitivityConfig(10, True, True, False, False, False, SensitivityMetricName.RETURN_PCT, SensitivityMetricName.STABILITY_SCORE, 1)
    res = ParameterSensitivityRunResult(
        "run_write", "utc", SensitivityRunStatus.COMPLETED, "strat", grid, config, [], [],
        {"return_pct": 10.0}, StabilityBucket.STABLE, OverfitRiskHint.LOW, [], [], {}, [], []
    )

    # 1. Result JSON
    f1 = write_sensitivity_result_json(d / "result.json", res)
    assert f1.exists()

    # 2. Grid JSON
    f2 = write_sensitivity_grid_json(d / "grid.json", grid, [])
    assert f2.exists()

    # 3. Aggregate Metrics JSON
    metrics = SensitivityAggregateMetrics(
        1, 0, 0, SensitivityMetricName.RETURN_PCT, 10.0, 10.0, 10.0, 10.0, 0.0, 0.0, 100.0, 0.0, 1.0, 0.0, [], []
    )
    f3 = write_sensitivity_aggregate_metrics_json(d / "metrics.json", metrics)
    assert f3.exists()

    # 4. Stability Map JSON
    smap = StabilityMap("map_1", "strat", SensitivityMetricName.RETURN_PCT, [], [], [], StabilityBucket.STABLE, [], [])
    f4 = write_stability_map_json(d / "map.json", smap)
    assert f4.exists()

def test_list_and_get_latest(tmp_path: Path):
    import time
    d1 = build_sensitivity_run_dir(tmp_path, "run_A")
    time.sleep(0.01)
    d2 = build_sensitivity_run_dir(tmp_path, "run_B")

    runs = list_sensitivity_runs(tmp_path)
    assert len(runs) == 2

    latest = get_latest_sensitivity_run_dir(tmp_path)
    assert latest is not None
    assert latest.name == "run_B"
