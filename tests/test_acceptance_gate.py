import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, BaselineComparisonStatus, RuntimeRegressionStatus, BaselineDriftDirection
from usa_signal_bot.performance.baseline_models import BaselineComparisonResult
from usa_signal_bot.performance.threshold_models import SLAEvaluationReport
from usa_signal_bot.performance.acceptance_gate import (
    evaluate_performance_acceptance_gate, build_performance_required_actions, build_performance_optional_actions, performance_acceptance_gate_result_to_text
)

def test_evaluate_performance_acceptance_gate_pass():
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, None, None, [], BaselineDriftDirection.FLAT, RuntimeRegressionStatus.NO_REGRESSION, [], [])
    r = SLAEvaluationReport("r1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, [], 0, 0, 0, 0, [], [])

    gate = evaluate_performance_acceptance_gate(PerformanceBaselineScope.SCAN, [c], [r])
    assert gate.status == BaselineComparisonStatus.PASS

def test_evaluate_performance_acceptance_gate_warn():
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.WARN, None, None, [], BaselineDriftDirection.WORSE, RuntimeRegressionStatus.MODERATE_REGRESSION, [], [])
    r = SLAEvaluationReport("r1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, [], 0, 0, 0, 0, [], [])

    gate = evaluate_performance_acceptance_gate(PerformanceBaselineScope.SCAN, [c], [r])
    assert gate.status == BaselineComparisonStatus.WARN

def test_evaluate_performance_acceptance_gate_fail():
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.FAIL, None, None, [], BaselineDriftDirection.WORSE, RuntimeRegressionStatus.MAJOR_REGRESSION, [], [])
    r = SLAEvaluationReport("r1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, [], 0, 0, 0, 0, [], [])

    gate = evaluate_performance_acceptance_gate(PerformanceBaselineScope.SCAN, [c], [r])
    assert gate.status == BaselineComparisonStatus.FAIL
    assert len(gate.required_actions) > 0

def test_evaluate_performance_acceptance_gate_blocked():
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, None, None, [], BaselineDriftDirection.WORSE, RuntimeRegressionStatus.NO_REGRESSION, [], [])
    r = SLAEvaluationReport("r1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.BLOCKED, [], 0, 0, 0, 1, [], [])

    gate = evaluate_performance_acceptance_gate(PerformanceBaselineScope.SCAN, [c], [r])
    assert gate.status == BaselineComparisonStatus.BLOCKED
    assert len(gate.required_actions) > 0

def test_performance_acceptance_gate_result_to_text():
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, None, None, [], BaselineDriftDirection.FLAT, RuntimeRegressionStatus.NO_REGRESSION, [], [])
    r = SLAEvaluationReport("r1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, [], 0, 0, 0, 0, [], [])
    gate = evaluate_performance_acceptance_gate(PerformanceBaselineScope.SCAN, [c], [r])
    txt = performance_acceptance_gate_result_to_text(gate)
    assert "Performance Acceptance Gate: PASS" in txt
