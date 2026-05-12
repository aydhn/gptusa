import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, BaselineComparisonStatus, PerformanceReportType, RuntimeRegressionStatus, BaselineDriftDirection
from usa_signal_bot.performance.baseline_models import PerformanceReviewResult, BaselineComparisonResult
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult
from usa_signal_bot.performance.quality_adapter import quality_issue_from_performance_gate, quality_dimension_score_from_performance_review, acceptance_warning_from_runtime_regression

def test_quality_issue_from_performance_gate():
    gate = PerformanceAcceptanceGateResult("g1", "", BaselineComparisonStatus.FAIL, PerformanceBaselineScope.SCAN, [], [], 0, 0, 1, 0, [], [], [], [])
    iss = quality_issue_from_performance_gate(gate)
    assert iss["issue_type"] == "PERFORMANCE_DEGRADATION"
    assert iss["severity"] == "HIGH"

    gate_pass = PerformanceAcceptanceGateResult("g2", "", BaselineComparisonStatus.PASS, PerformanceBaselineScope.SCAN, [], [], 1, 0, 0, 0, [], [], [], [])
    iss2 = quality_issue_from_performance_gate(gate_pass)
    assert not iss2

def test_quality_dimension_score_from_performance_review():
    rev = PerformanceReviewResult("r1", "", PerformanceReportType.FULL_PERFORMANCE_REVIEW, BaselineComparisonStatus.PASS, [], [], [], [], [], BaselineComparisonStatus.WARN, {}, [], [])
    score = quality_dimension_score_from_performance_review(rev)
    assert score["dimension"] == "runtime_performance"
    assert score["score"] == 80.0

def test_acceptance_warning_from_runtime_regression():
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.FAIL, None, None, [], BaselineDriftDirection.WORSE, RuntimeRegressionStatus.MAJOR_REGRESSION, [], [])
    w = acceptance_warning_from_runtime_regression(c)
    assert "MAJOR_REGRESSION detected" in w

    c2 = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, None, None, [], BaselineDriftDirection.FLAT, RuntimeRegressionStatus.NO_REGRESSION, [], [])
    w2 = acceptance_warning_from_runtime_regression(c2)
    assert w2 is None
