import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, BaselineComparisonStatus
from usa_signal_bot.performance.scheduler_adapter import performance_sample_from_scheduler_run, scheduler_hints_from_performance_gate, annotate_scheduler_plan_with_performance_gate
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult

def test_performance_sample_from_scheduler_run():
    s = performance_sample_from_scheduler_run({})
    assert s.scope == PerformanceBaselineScope.SCHEDULER

def test_scheduler_hints_from_performance_gate():
    gate = PerformanceAcceptanceGateResult("g1", "", BaselineComparisonStatus.BLOCKED, PerformanceBaselineScope.SCAN, [], [], 0, 0, 0, 1, [], [], [], [])
    hints = scheduler_hints_from_performance_gate(gate)
    assert hints["action"] == "BLOCK"
    assert hints["delay_minutes"] == 120

def test_annotate_scheduler_plan_with_performance_gate():
    class DummyPlan:
        pass
    p = DummyPlan()
    gate = PerformanceAcceptanceGateResult("g1", "", BaselineComparisonStatus.WARN, PerformanceBaselineScope.SCAN, [], [], 0, 1, 0, 0, [], [], [], [])
    p2 = annotate_scheduler_plan_with_performance_gate(p, gate)
    assert p2.metadata["performance_gate_status"] == "WARN"
    assert p2.metadata["performance_hints"]["action"] == "REVIEW"
