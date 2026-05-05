import pytest
from pathlib import Path
from usa_signal_bot.core.enums import ParameterGridType, SensitivityRunStatus, StabilityBucket, OverfitRiskHint, SensitivityMetricName
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterGridSpec, ParameterSensitivityConfig, ParameterSensitivityRunResult
)
from usa_signal_bot.backtesting.sensitivity_reporting import (
    parameter_grid_spec_to_text, sensitivity_summary_to_text,
    parameter_sensitivity_run_result_to_text, sensitivity_limitations_text,
    write_sensitivity_report_json
)

def create_fake_result():
    grid = ParameterGridSpec("g1", "strat", ParameterGridType.SINGLE_PARAMETER, [], 10)
    config = ParameterSensitivityConfig(10, True, True, False, False, False, SensitivityMetricName.RETURN_PCT, SensitivityMetricName.STABILITY_SCORE, 1)
    res = ParameterSensitivityRunResult(
        "run1", "utc", SensitivityRunStatus.COMPLETED, "strat", grid, config, [], [],
        {"return_pct": 10.0}, StabilityBucket.STABLE, OverfitRiskHint.LOW, [], [], {}, [], []
    )
    return res

def test_parameter_grid_spec_to_text():
    grid = ParameterGridSpec("g1", "strat", ParameterGridType.SINGLE_PARAMETER, [], 10)
    txt = parameter_grid_spec_to_text(grid)
    assert "g1" in txt
    assert "strat" in txt
    assert "SINGLE_PARAMETER" in txt

def test_sensitivity_summary_to_text():
    res = create_fake_result()
    txt = sensitivity_summary_to_text(res)
    assert "run1" in txt
    assert "COMPLETED" in txt
    assert "STABLE" in txt

def test_parameter_sensitivity_run_result_to_text():
    res = create_fake_result()
    txt = parameter_sensitivity_run_result_to_text(res)
    assert "PARAMETER SENSITIVITY RUN RESULT" in txt
    assert "run1" in txt
    assert "best_params" not in txt.lower()
    assert "optimal" not in txt.lower()

def test_sensitivity_limitations_text():
    txt = sensitivity_limitations_text()
    assert "LIMITATIONS AND WARNINGS" in txt
    assert "NOT perform optimization" in txt

def test_write_sensitivity_report_json(tmp_path: Path):
    res = create_fake_result()
    f = write_sensitivity_report_json(tmp_path / "report.json", res)
    assert f.exists()
    content = f.read_text()
    assert "LIMITATIONS AND WARNINGS" in content
    assert "run1" in content
