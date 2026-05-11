import pytest
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
