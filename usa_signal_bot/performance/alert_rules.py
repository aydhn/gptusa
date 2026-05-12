from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import uuid

from usa_signal_bot.core.enums import (
    PerformanceBaselineScope,
    PerformanceMetricName,
    RuntimeRegressionStatus,
    SLASeverity,
    PerformanceAlertStatus,
    BaselineComparisonStatus
)
from usa_signal_bot.performance.baseline_models import BaselineComparisonResult
from usa_signal_bot.performance.threshold_models import SLAEvaluationReport

@dataclass
class PerformanceAlertRule:
    rule_id: str
    name: str
    enabled: bool
    scope: PerformanceBaselineScope
    metric_name: Optional[PerformanceMetricName]
    min_regression_status: RuntimeRegressionStatus
    severity: SLASeverity
    suppress_if_insufficient_data: bool = True
    description: Optional[str] = None

@dataclass
class PerformanceAlert:
    alert_id: str
    created_at_utc: str
    status: PerformanceAlertStatus
    rule_id: str
    scope: PerformanceBaselineScope
    severity: SLASeverity
    title: str
    message: str
    evidence: Dict[str, Any]
    warnings: List[str]
    errors: List[str]

def create_performance_alert_rule_id(name: str) -> str:
    return f"perf_rule_{name.replace(' ', '_').lower()}"

def create_performance_alert_id(prefix: str = "perf_alert") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def default_performance_alert_rules() -> List[PerformanceAlertRule]:
    return [
        PerformanceAlertRule(
            rule_id=create_performance_alert_rule_id("critical_regression_all"),
            name="Critical Regression Default",
            enabled=True,
            scope=PerformanceBaselineScope.FULL_LOCAL_STACK,
            metric_name=None,
            min_regression_status=RuntimeRegressionStatus.CRITICAL_REGRESSION,
            severity=SLASeverity.BLOCKER,
            description="Catch all critical regressions."
        ),
        PerformanceAlertRule(
            rule_id=create_performance_alert_rule_id("major_regression_all"),
            name="Major Regression Default",
            enabled=True,
            scope=PerformanceBaselineScope.FULL_LOCAL_STACK,
            metric_name=None,
            min_regression_status=RuntimeRegressionStatus.MAJOR_REGRESSION,
            severity=SLASeverity.CRITICAL,
            description="Catch all major regressions."
        )
    ]

def evaluate_performance_alert_rule(rule: PerformanceAlertRule, comparison: BaselineComparisonResult, threshold_report: Optional[SLAEvaluationReport] = None) -> Optional[PerformanceAlert]:
    if not rule.enabled:
        return None

    if comparison.status == BaselineComparisonStatus.INSUFFICIENT_DATA and rule.suppress_if_insufficient_data:
        return None

    if rule.scope != PerformanceBaselineScope.FULL_LOCAL_STACK and rule.scope != comparison.scope:
        return None

    # very simple rank check assuming ordinal values align conceptually
    rank_map = {
        RuntimeRegressionStatus.NO_REGRESSION: 0,
        RuntimeRegressionStatus.INSUFFICIENT_DATA: 0,
        RuntimeRegressionStatus.MINOR_REGRESSION: 1,
        RuntimeRegressionStatus.MODERATE_REGRESSION: 2,
        RuntimeRegressionStatus.MAJOR_REGRESSION: 3,
        RuntimeRegressionStatus.CRITICAL_REGRESSION: 4
    }

    obs_rank = rank_map.get(comparison.regression_status, 0)
    req_rank = rank_map.get(rule.min_regression_status, 4)

    if obs_rank >= req_rank and obs_rank > 0:
        return PerformanceAlert(
            alert_id=create_performance_alert_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=PerformanceAlertStatus.CREATED,
            rule_id=rule.rule_id,
            scope=comparison.scope,
            severity=rule.severity,
            title=f"Performance Alert: {comparison.regression_status.value}",
            message=f"Rule {rule.name} triggered by {comparison.regression_status.value} on scope {comparison.scope.value}. Please review.",
            evidence={"comparison_id": comparison.comparison_id},
            warnings=[], errors=[]
        )

    # Also check SLA report for breaches
    if threshold_report:
        for ev in threshold_report.evaluations:
            if ev.severity in [SLASeverity.CRITICAL, SLASeverity.BLOCKER] and ev.status in [BaselineComparisonStatus.FAIL, BaselineComparisonStatus.BLOCKED]:
                 return PerformanceAlert(
                    alert_id=create_performance_alert_id(),
                    created_at_utc=datetime.now(timezone.utc).isoformat(),
                    status=PerformanceAlertStatus.CREATED,
                    rule_id=rule.rule_id,
                    scope=threshold_report.scope,
                    severity=ev.severity,
                    title=f"SLA Breach: {ev.metric_name.value}",
                    message=f"Rule {rule.name} triggered by SLA {ev.status.value} on {ev.metric_name.value}. {ev.message}",
                    evidence={"evaluation_id": ev.evaluation_id},
                    warnings=[], errors=[]
                )

    return None

def build_performance_alerts(comparisons: List[BaselineComparisonResult], threshold_reports: Optional[List[SLAEvaluationReport]] = None, rules: Optional[List[PerformanceAlertRule]] = None) -> List[PerformanceAlert]:
    alerts = []
    active_rules = rules if rules is not None else default_performance_alert_rules()
    reports_map = {r.scope: r for r in (threshold_reports or [])}

    for c in comparisons:
        rep = reports_map.get(c.scope)
        for r in active_rules:
            alert = evaluate_performance_alert_rule(r, c, rep)
            if alert:
                alerts.append(alert)

    return alerts

def performance_alert_rule_to_dict(rule: PerformanceAlertRule) -> Dict[str, Any]:
    return {
        "rule_id": rule.rule_id,
        "name": rule.name,
        "enabled": rule.enabled,
        "scope": rule.scope.value,
        "metric_name": rule.metric_name.value if rule.metric_name else None,
        "min_regression_status": rule.min_regression_status.value,
        "severity": rule.severity.value,
        "suppress_if_insufficient_data": rule.suppress_if_insufficient_data,
        "description": rule.description
    }

def performance_alert_to_dict(alert: PerformanceAlert) -> Dict[str, Any]:
    return {
        "alert_id": alert.alert_id,
        "created_at_utc": alert.created_at_utc,
        "status": alert.status.value,
        "rule_id": alert.rule_id,
        "scope": alert.scope.value,
        "severity": alert.severity.value,
        "title": alert.title,
        "message": alert.message,
        "evidence": alert.evidence,
        "warnings": alert.warnings,
        "errors": alert.errors
    }

def performance_alerts_to_text(alerts: List[PerformanceAlert], limit: int = 50) -> str:
    if not alerts:
        return "No Performance Alerts."
    lines = [f"Performance Alerts ({len(alerts)}):"]
    for a in alerts[:limit]:
        lines.append(f"[{a.severity.value}] {a.title} - {a.message}")
    return "\n".join(lines)
