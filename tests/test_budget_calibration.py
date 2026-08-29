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


def test_budget_calibration_result_to_text():
    from usa_signal_bot.profiling.budget_calibration import budget_calibration_result_to_text
    from usa_signal_bot.profiling.profiling_models import BudgetCalibrationResult
    from unittest.mock import MagicMock
    result1 = BudgetCalibrationResult(calibration_id="cal1", created_at_utc="2023-01-01T00:00:00Z", status=MagicMock(value="CALIBRATED"), scope=MagicMock(value="TASK"), sample_count=5, decision=MagicMock(value="RAISE_BUDGET"), current_budget={"wall_time_seconds": 10}, recommended_budget={"wall_time_seconds": 20}, confidence=0.8, evidence={}, warnings=[], errors=[])
    text1 = budget_calibration_result_to_text(result1)
    assert "Calibration for TASK (Samples: 5)" in text1
    assert "Status: CALIBRATED" in text1
    assert "Decision: RAISE_BUDGET" in text1
    assert "Confidence: 0.80" in text1

    result2 = BudgetCalibrationResult(calibration_id="cal2", created_at_utc="2023-01-01T00:00:00Z", status=MagicMock(value="INSUFFICIENT_DATA"), scope=MagicMock(value="TASK"), sample_count=1, decision=MagicMock(value="REVIEW_REQUIRED"), current_budget={"wall_time_seconds": 10}, recommended_budget={"wall_time_seconds": 10}, confidence=None, evidence={}, warnings=[], errors=[])
    text2 = budget_calibration_result_to_text(result2)
    assert "Calibration for TASK (Samples: 1)" in text2
    assert "Status: INSUFFICIENT_DATA" in text2
    assert "Decision: REVIEW_REQUIRED" in text2
    assert "Confidence: N/A" in text2
