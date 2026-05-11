import pytest
from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus, ResourceMetricName, CalibrationStatus, CalibrationDecision, ThrottlingAction, ThrottlingSeverity, ThrottlingReason
from usa_signal_bot.profiling.profiling_models import (
    ResourceMetric, ResourceProfile, BudgetCalibrationInput, BudgetCalibrationResult,
    ThrottlingRecommendation, ThrottlingPlan, ProfilingReviewResult,
    create_resource_metric_id, create_resource_profile_id, validate_resource_metric, validate_resource_profile, validate_budget_calibration_result, validate_throttling_plan
)
from usa_signal_bot.core.exceptions import ProfilingValidationError

def test_resource_metric_creation_and_validation():
    metric = ResourceMetric(
        metric_id=create_resource_metric_id(), name=ResourceMetricName.WALL_TIME_SECONDS, value=1.5,
        unit="seconds", status=ResourceProfileStatus.COMPLETED, source="test", created_at_utc="utc"
    )
    validate_resource_metric(metric)

def test_validation_errors():
    profile = ResourceProfile("id", ResourceProfileScope.TASK, "task", ResourceProfileStatus.COMPLETED, None, None, -1.0, 0, 0, 0, 0, 0, 0, 0, [], [], [])
    with pytest.raises(ProfilingValidationError, match="Negative wall_time_seconds"):
        validate_resource_profile(profile)
