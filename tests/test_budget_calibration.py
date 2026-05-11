import pytest
from usa_signal_bot.core.enums import ResourceProfileScope, CalibrationStatus, CalibrationDecision, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceProfile
from usa_signal_bot.profiling.budget_calibration import calibrate_budget_for_scope

def create_mock_profile(wall_time: float, memory_peak: int):
    return ResourceProfile("id", ResourceProfileScope.TASK, "target", ResourceProfileStatus.COMPLETED,
                          None, None, wall_time, 0, 0, memory_peak, 0, 0, 0, 0, [], [], [])

def test_calibrate_insufficient_data():
    profiles = [create_mock_profile(10.0, 1024)]
    budget = {"wall_time_seconds": 10.0, "memory_peak_bytes": 1024}

    result = calibrate_budget_for_scope(ResourceProfileScope.TASK, profiles, budget)
    assert result.status == CalibrationStatus.INSUFFICIENT_DATA
    assert result.decision == CalibrationDecision.REVIEW_REQUIRED

def test_calibrate_calibrated():
    profiles = [create_mock_profile(10.0, 1024), create_mock_profile(11.0, 1024), create_mock_profile(12.0, 1024)]
    budget = {"wall_time_seconds": 100.0, "memory_peak_bytes": 10240}

    result = calibrate_budget_for_scope(ResourceProfileScope.TASK, profiles, budget)
    assert result.status == CalibrationStatus.CALIBRATED
    assert result.decision == CalibrationDecision.LOWER_BUDGET

def test_calibrate_raise_budget():
    profiles = [create_mock_profile(100.0, 1024), create_mock_profile(110.0, 1024), create_mock_profile(120.0, 1024)]
    budget = {"wall_time_seconds": 10.0, "memory_peak_bytes": 10240}

    result = calibrate_budget_for_scope(ResourceProfileScope.TASK, profiles, budget)
    assert result.status == CalibrationStatus.CALIBRATED
    assert result.decision in [CalibrationDecision.SPLIT_TASK, CalibrationDecision.RAISE_BUDGET]
