import pytest
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BaselineComparisonReport, RelativePerformanceValidationReport, BenchmarkSafetyBoundaryResult
from usa_signal_bot.backtesting.benchmark_comparison.phase150_readiness_gate import build_phase150_readiness_gate

def test_phase150_gate():
    report = BaselineComparisonReport(report_id="r1", created_at_utc="", run_id="run1", report_valid=True)
    val = RelativePerformanceValidationReport(validation_id="v1", created_at_utc="", validation_passed=True)
    boundary = BenchmarkSafetyBoundaryResult(boundary_id="b1", created_at_utc="", boundary_passed=True)

    gate = build_phase150_readiness_gate(report, val, boundary)
    assert gate.ready_for_phase150 is True
