import pytest
from usa_signal_bot.core.enums import PerformanceBaselineScope, RuntimeRegressionStatus, SLASeverity, BaselineComparisonStatus, BaselineDriftDirection
from usa_signal_bot.performance.baseline_models import BaselineComparisonResult
from usa_signal_bot.performance.alert_rules import (
    PerformanceAlertRule, default_performance_alert_rules, evaluate_performance_alert_rule, build_performance_alerts, performance_alerts_to_text
)

def test_default_performance_alert_rules():
    rules = default_performance_alert_rules()
    assert len(rules) > 0

def test_evaluate_performance_alert_rule_match():
    r = PerformanceAlertRule("r1", "rule", True, PerformanceBaselineScope.FULL_LOCAL_STACK, None, RuntimeRegressionStatus.MAJOR_REGRESSION, SLASeverity.CRITICAL)
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.FAIL, None, None, [], BaselineDriftDirection.WORSE, RuntimeRegressionStatus.MAJOR_REGRESSION, [], [])

    alert = evaluate_performance_alert_rule(r, c)
    assert alert is not None
    assert alert.severity == SLASeverity.CRITICAL

def test_evaluate_performance_alert_rule_no_match():
    r = PerformanceAlertRule("r1", "rule", True, PerformanceBaselineScope.FULL_LOCAL_STACK, None, RuntimeRegressionStatus.MAJOR_REGRESSION, SLASeverity.CRITICAL)
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.PASS, None, None, [], BaselineDriftDirection.FLAT, RuntimeRegressionStatus.MINOR_REGRESSION, [], [])

    alert = evaluate_performance_alert_rule(r, c)
    assert alert is None

def test_evaluate_performance_alert_rule_suppress_insufficient():
    r = PerformanceAlertRule("r1", "rule", True, PerformanceBaselineScope.FULL_LOCAL_STACK, None, RuntimeRegressionStatus.MAJOR_REGRESSION, SLASeverity.CRITICAL, True)
    c = BaselineComparisonResult("c1", "", PerformanceBaselineScope.SCAN, BaselineComparisonStatus.INSUFFICIENT_DATA, None, None, [], BaselineDriftDirection.UNKNOWN, RuntimeRegressionStatus.INSUFFICIENT_DATA, [], [])

    alert = evaluate_performance_alert_rule(r, c)
    assert alert is None

def test_performance_alerts_to_text():
    alerts = build_performance_alerts([])
    txt = performance_alerts_to_text(alerts)
    assert "No Performance Alerts." in txt
