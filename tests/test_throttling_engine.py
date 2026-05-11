import pytest
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
