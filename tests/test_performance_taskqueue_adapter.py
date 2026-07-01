import pytest
from usa_signal_bot.core.enums import BaselineComparisonStatus, PerformanceBaselineScope
from usa_signal_bot.performance.taskqueue_adapter import performance_sample_from_taskqueue_run, taskqueue_budget_adjustments_from_performance_gate, annotate_taskqueue_plan_with_performance_baseline
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult

def test_performance_sample_from_taskqueue_run():
    s = performance_sample_from_taskqueue_run({"created_at_utc": "time"})
    assert s.scope == PerformanceBaselineScope.TASKQUEUE

def test_taskqueue_budget_adjustments_from_performance_gate():
    gate = PerformanceAcceptanceGateResult("g1", "", BaselineComparisonStatus.BLOCKED, PerformanceBaselineScope.SCAN, [], [], 0, 0, 0, 1, [], [], [], [])
    adj = taskqueue_budget_adjustments_from_performance_gate(gate)
    assert adj["cpu_budget_modifier"] == 0.5
    assert "BLOCKED" in adj["reason"]

def test_annotate_taskqueue_plan_with_performance_baseline():
    class DummyPlan:
        pass
    p = DummyPlan()
    gate = PerformanceAcceptanceGateResult("g1", "", BaselineComparisonStatus.FAIL, PerformanceBaselineScope.SCAN, [], [], 0, 0, 1, 0, [], [], [], [])

    p2 = annotate_taskqueue_plan_with_performance_baseline(p, None, gate)
    assert p2.metadata["performance_gate_status"] == "FAIL"
    assert p2.metadata["budget_adjustments"]["cpu_budget_modifier"] == 0.75

from unittest.mock import patch

def test_annotate_taskqueue_plan_with_performance_baseline_exception():
    class BrokenPlan:
        @property
        def metadata(self):
            raise ValueError("Test error")

    p = BrokenPlan()
    with patch('usa_signal_bot.performance.taskqueue_adapter.logger.warning') as mock_warning:
        p2 = annotate_taskqueue_plan_with_performance_baseline(p, "dummy_baseline", None)
        assert p2 == p
        mock_warning.assert_called_once()
