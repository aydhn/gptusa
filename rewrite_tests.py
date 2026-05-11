test_run_metrics_loader = """import pytest
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
"""
with open('tests/test_run_metrics_loader.py', 'w') as f: f.write(test_run_metrics_loader)


test_resource_profile_collector = """import pytest
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
"""
with open('tests/test_resource_profile_collector.py', 'w') as f: f.write(test_resource_profile_collector)


test_budget_calibration = """import pytest
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
"""
with open('tests/test_budget_calibration.py', 'w') as f: f.write(test_budget_calibration)


test_throttling_policy = """import pytest
from usa_signal_bot.core.enums import ResourceProfileScope
from usa_signal_bot.core.exceptions import ThrottlingPolicyError
from usa_signal_bot.profiling.throttling_policy import default_throttling_policies, policy_for_profile_scope, validate_throttling_policy

def test_default_policies():
    policies = default_throttling_policies()
    assert len(policies) > 0
    assert any(p.scope == ResourceProfileScope.SCAN for p in policies)

def test_policy_for_profile_scope():
    policies = default_throttling_policies()
    scan_policy = policy_for_profile_scope(ResourceProfileScope.SCAN, policies)
    assert scan_policy.scope == ResourceProfileScope.SCAN

    unknown_policy = policy_for_profile_scope(ResourceProfileScope.CUSTOM, policies)
    assert unknown_policy.scope == ResourceProfileScope.CUSTOM

def test_validate_throttling_policy():
    policies = default_throttling_policies()
    validate_throttling_policy(policies[0])

    bad_policy = policies[0]
    bad_policy.max_wall_time_seconds = -1.0

    with pytest.raises(ThrottlingPolicyError):
        validate_throttling_policy(bad_policy)
"""
with open('tests/test_throttling_policy.py', 'w') as f: f.write(test_throttling_policy)


test_throttling_engine = """import pytest
from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus, ThrottlingSeverity, ThrottlingAction, ThrottlingReason
from usa_signal_bot.profiling.profiling_models import ResourceProfile
from usa_signal_bot.profiling.throttling_engine import AdaptiveThrottlingEngine

def create_mock_profile(wall_time: float, memory_peak: int, scope: ResourceProfileScope = ResourceProfileScope.SCAN):
    return ResourceProfile("id", scope, "target", ResourceProfileStatus.COMPLETED,
                          None, None, wall_time, 0, 0, memory_peak, 0, 0, 0, 0, [], [], [])

def test_throttling_engine_normal_profile():
    engine = AdaptiveThrottlingEngine()
    profile = create_mock_profile(10.0, 1024)
    recs = engine.evaluate_profile(profile)
    assert len(recs) == 0

def test_throttling_engine_critical_time():
    engine = AdaptiveThrottlingEngine()
    profile = create_mock_profile(2000.0, 1024)
    recs = engine.evaluate_profile(profile)
    assert len(recs) == 1
    assert recs[0].severity == ThrottlingSeverity.CRITICAL
    assert ThrottlingReason.TIME_BUDGET in recs[0].reasons
    assert recs[0].action == ThrottlingAction.REDUCE_SCOPE

def test_throttling_engine_insufficient_data():
    engine = AdaptiveThrottlingEngine()
    profile = create_mock_profile(10.0, 1024)
    profile.status = ResourceProfileStatus.INSUFFICIENT_DATA

    recs = engine.evaluate_profile(profile)
    assert len(recs) == 1
    assert recs[0].severity == ThrottlingSeverity.MODERATE
    assert recs[0].action == ThrottlingAction.REVIEW
    assert ThrottlingReason.INSUFFICIENT_PROFILE_DATA in recs[0].reasons

def test_build_plan():
    engine = AdaptiveThrottlingEngine()
    profiles = [create_mock_profile(10.0, 1024), create_mock_profile(2000.0, 1024)]
    plan = engine.build_plan(profiles)
    assert len(plan.recommendations) == 1
"""
with open('tests/test_throttling_engine.py', 'w') as f: f.write(test_throttling_engine)


test_taskqueue_adapter = """import pytest
from usa_signal_bot.core.enums import ResourceProfileScope, ThrottlingAction, ThrottlingSeverity
from usa_signal_bot.profiling.profiling_models import ResourceProfile, ThrottlingRecommendation, ThrottlingPlan
from usa_signal_bot.profiling.taskqueue_adapter import adjusted_workload_budget_from_calibration, apply_throttling_to_local_task, taskqueue_budget_hints_from_profiles, taskqueue_plan_with_throttling_hints

class DummyTask:
    def __init__(self, task_id):
        self.task_id = task_id
        self.metadata = {}

class DummyPlan:
    def __init__(self):
        self.metadata = {}

def test_adjusted_workload_budget_from_calibration():
    budget = {"x": 1}
    assert adjusted_workload_budget_from_calibration(budget, []) == budget

def test_apply_throttling_to_local_task():
    task = DummyTask("task_1")
    rec1 = ThrottlingRecommendation("id1", "task_1", ResourceProfileScope.TASK, ThrottlingAction.DRY_RUN_ONLY, ThrottlingSeverity.CRITICAL, [], "msg", {}, {})
    modified_task = apply_throttling_to_local_task(task, [rec1])
    assert modified_task.metadata.get("throttling_hint") == "DRY_RUN_ONLY"

def test_taskqueue_budget_hints_from_profiles():
    prof = ResourceProfile("id", ResourceProfileScope.TASK, "test", "COMPLETED", None, None, 1.0, 0, 0, 1024, 0, 0, 0, 0, [], [], [])
    hints = taskqueue_budget_hints_from_profiles([prof])
    assert "test" in hints

def test_taskqueue_plan_with_throttling_hints():
    plan = DummyPlan()
    t_plan = ThrottlingPlan("id", "utc", "COMPLETED", [], 1, 2, 3, {}, [], [])
    mod_plan = taskqueue_plan_with_throttling_hints(plan, t_plan)
    assert mod_plan.metadata["throttling_review_count"] == 3
"""
with open('tests/test_taskqueue_adapter.py', 'w') as f: f.write(test_taskqueue_adapter)


test_scheduler_adapter = """import pytest
from usa_signal_bot.core.enums import ResourceProfileScope, ThrottlingAction, ThrottlingSeverity
from usa_signal_bot.profiling.profiling_models import ThrottlingPlan, ThrottlingRecommendation
from usa_signal_bot.profiling.scheduler_adapter import scheduler_hints_from_throttling_plan, annotate_scheduler_plan_with_resource_hints, should_scheduler_delay_scope

class DummyPlan:
    def __init__(self):
        self.metadata = {}

def test_scheduler_hints_from_throttling_plan():
    rec1 = ThrottlingRecommendation("id1", "task_1", ResourceProfileScope.SCAN, ThrottlingAction.DELAY, ThrottlingSeverity.CRITICAL, [], "msg", {}, {})
    plan = ThrottlingPlan("id", "utc", "COMPLETED", [rec1], 0, 0, 0, {}, [], [])
    hints = scheduler_hints_from_throttling_plan(plan)
    assert "SCAN" in hints["delay_scopes"]

def test_annotate_scheduler_plan_with_resource_hints():
    plan = DummyPlan()
    rec1 = ThrottlingRecommendation("id1", "task_1", ResourceProfileScope.SCAN, ThrottlingAction.REVIEW, ThrottlingSeverity.MODERATE, [], "msg", {}, {})
    t_plan = ThrottlingPlan("id", "utc", "COMPLETED", [rec1], 0, 0, 0, {}, [], [])
    mod_plan = annotate_scheduler_plan_with_resource_hints(plan, t_plan)
    assert "SCAN" in mod_plan.metadata["throttling_hints"]["review_scopes"]

def test_should_scheduler_delay_scope():
    rec1 = ThrottlingRecommendation("id1", "task_1", ResourceProfileScope.SCAN, ThrottlingAction.DELAY, ThrottlingSeverity.CRITICAL, [], "msg", {}, {})
    plan = ThrottlingPlan("id", "utc", "COMPLETED", [rec1], 0, 0, 0, {}, [], [])
    assert should_scheduler_delay_scope(ResourceProfileScope.SCAN, plan) is True
"""
with open('tests/test_scheduler_adapter.py', 'w') as f: f.write(test_scheduler_adapter)


test_profiling_models = """import pytest
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
"""
with open('tests/test_profiling_models.py', 'w') as f: f.write(test_profiling_models)
