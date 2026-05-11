import pytest
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
