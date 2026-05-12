import pytest
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName, SLAThresholdType, SLASeverity, BaselineComparisonStatus
from usa_signal_bot.performance.threshold_models import (
    SLAThreshold, SLAThresholdEvaluation, SLAEvaluationReport,
    create_sla_threshold_id, create_sla_evaluation_id, create_sla_report_id,
    validate_sla_threshold, validate_sla_evaluation_report,
    sla_threshold_to_dict, sla_threshold_evaluation_to_dict, sla_evaluation_report_to_dict
)
from usa_signal_bot.core.exceptions import PerformanceBaselineValidationError

def test_sla_threshold_valid():
    t = SLAThreshold(
        threshold_id="t1", name="Wall Time", scope=PerformanceBaselineScope.SCAN, metric_name=PerformanceMetricName.WALL_TIME_SECONDS,
        threshold_type=SLAThresholdType.MAX, warning_value=100, critical_value=200, blocker_value=300, enabled=True,
        severity=SLASeverity.WARNING, description=None, metadata={}
    )
    validate_sla_threshold(t)
    assert t.name == "Wall Time"

def test_sla_threshold_invalid_order():
    t = SLAThreshold(
        threshold_id="t1", name="Wall Time", scope=PerformanceBaselineScope.SCAN, metric_name=PerformanceMetricName.WALL_TIME_SECONDS,
        threshold_type=SLAThresholdType.MAX, warning_value=100, critical_value=200, blocker_value=150, enabled=True,
        severity=SLASeverity.WARNING, description=None, metadata={}
    )
    with pytest.raises(PerformanceBaselineValidationError):
        validate_sla_threshold(t)

def test_sla_evaluation_report_serialization():
    e = SLAThresholdEvaluation(
        evaluation_id="e1", created_at_utc=datetime.now(timezone.utc).isoformat(), threshold_id="t1",
        scope=PerformanceBaselineScope.SCAN, metric_name=PerformanceMetricName.WALL_TIME_SECONDS,
        observed_value=150, baseline_value=100, status=BaselineComparisonStatus.WARN, severity=SLASeverity.WARNING,
        message="warn", evidence={}, warnings=[], errors=[]
    )
    rep = SLAEvaluationReport(
        report_id="r1", created_at_utc=datetime.now(timezone.utc).isoformat(), scope=PerformanceBaselineScope.SCAN,
        status=BaselineComparisonStatus.WARN, evaluations=[e], pass_count=0, warn_count=1, fail_count=0, blocked_count=0,
        warnings=[], errors=[]
    )
    validate_sla_evaluation_report(rep)
    d = sla_evaluation_report_to_dict(rep)
    assert d["report_id"] == "r1"
    assert len(d["evaluations"]) == 1

def test_id_factories_thresholds():
    assert create_sla_threshold_id(PerformanceBaselineScope.SCAN, PerformanceMetricName.WALL_TIME_SECONDS)
    assert create_sla_evaluation_id()
    assert create_sla_report_id()
