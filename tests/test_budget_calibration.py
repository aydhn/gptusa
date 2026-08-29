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


from unittest.mock import patch, MagicMock

def test_calibrate_all_budgets_happy_path():
    from usa_signal_bot.profiling.budget_calibration import calibrate_all_budgets
    mock_profile = MagicMock()
    mock_result = MagicMock()
    with patch('usa_signal_bot.profiling.budget_calibration.ResourceProfileScope') as mock_scope_class, patch('usa_signal_bot.profiling.budget_calibration.calibrate_budget_for_scope', return_value=mock_result) as mock_calibrate:
        mock_scope_instance = MagicMock()
        mock_scope_class.return_value = mock_scope_instance
        results = calibrate_all_budgets([mock_profile], {'VALID_SCOPE': {'wall_time_seconds': 10.0}})
        assert len(results) == 1
        assert results[0] == mock_result
        mock_scope_class.assert_called_once_with('VALID_SCOPE')
        mock_calibrate.assert_called_once_with(mock_scope_instance, [mock_profile], {'wall_time_seconds': 10.0})

def test_calibrate_all_budgets_value_error():
    from usa_signal_bot.profiling.budget_calibration import calibrate_all_budgets
    with patch('usa_signal_bot.profiling.budget_calibration.ResourceProfileScope', side_effect=ValueError):
        results = calibrate_all_budgets([], {'INVALID_SCOPE': {'wall_time_seconds': 10.0}})
        assert len(results) == 0
