from typing import List, Optional

from usa_signal_bot.core.enums import (
    AlertConditionOperator,
    AlertPolicyScope,
    AlertRouteTarget,
    AlertSeverity,
    AlertType,
    NotificationPriority,
    NotificationType
)
from usa_signal_bot.notifications.alert_models import AlertCondition, AlertPolicy

def default_alert_policies() -> List[AlertPolicy]:
    policies = []
    policies.extend(scan_alert_policies())
    policies.extend(candidate_alert_policies())
    policies.extend(risk_alert_policies())
    policies.extend(portfolio_alert_policies())
    policies.extend(runtime_alert_policies())
    policies.extend(health_alert_policies())
    return policies

def scan_alert_policies() -> List[AlertPolicy]:
    return [
        AlertPolicy(
            policy_id="scan_completed_notice",
            name="Scan Completed Notice",
            scope=AlertPolicyScope.SCAN,
            alert_type=AlertType.SCAN_COMPLETED,
            enabled=True,
            severity=AlertSeverity.NOTICE,
            min_severity_to_route=AlertSeverity.INFO,
            conditions=[
                AlertCondition(
                    name="status_completed",
                    field_path="status",
                    operator=AlertConditionOperator.IN,
                    threshold=["COMPLETED", "PARTIAL_SUCCESS", "completed", "partial_success"]
                )
            ],
            route_target=AlertRouteTarget.DRY_RUN,
            notification_type=NotificationType.SCAN_SUMMARY,
            priority=NotificationPriority.NORMAL,
            cooldown_seconds=1800,
            suppress_duplicates=True,
            max_alerts_per_run=1
        ),
        AlertPolicy(
            policy_id="scan_failed_warning",
            name="Scan Failed Warning",
            scope=AlertPolicyScope.SCAN,
            alert_type=AlertType.SCAN_FAILED,
            enabled=True,
            severity=AlertSeverity.HIGH,
            min_severity_to_route=AlertSeverity.INFO,
            conditions=[
                AlertCondition(
                    name="status_failed",
                    field_path="status",
                    operator=AlertConditionOperator.IN,
                    threshold=["FAILED", "STOPPED", "failed", "stopped"]
                )
            ],
            route_target=AlertRouteTarget.LOG_ONLY,
            notification_type=NotificationType.SCAN_SUMMARY,
            priority=NotificationPriority.HIGH,
            cooldown_seconds=300,
            suppress_duplicates=True,
            max_alerts_per_run=1
        )
    ]

def candidate_alert_policies() -> List[AlertPolicy]:
    return [
        AlertPolicy(
            policy_id="high_quality_candidate",
            name="High Quality Candidate",
            scope=AlertPolicyScope.CANDIDATE,
            alert_type=AlertType.HIGH_QUALITY_CANDIDATE,
            enabled=True,
            severity=AlertSeverity.HIGH,
            min_severity_to_route=AlertSeverity.INFO,
            conditions=[
                AlertCondition(
                    name="candidate_count_gt_zero",
                    field_path="candidate_count",
                    operator=AlertConditionOperator.GT,
                    threshold=0
                )
            ],
            route_target=AlertRouteTarget.LOG_ONLY,
            notification_type=NotificationType.SIGNAL_CANDIDATE,
            priority=NotificationPriority.HIGH,
            cooldown_seconds=1800,
            suppress_duplicates=True,
            max_alerts_per_run=5
        )
    ]

def risk_alert_policies() -> List[AlertPolicy]:
    return [
        AlertPolicy(
            policy_id="risk_rejected_warning",
            name="Risk Rejected Warning",
            scope=AlertPolicyScope.RISK,
            alert_type=AlertType.RISK_REJECTED_WARNING,
            enabled=True,
            severity=AlertSeverity.WARNING,
            min_severity_to_route=AlertSeverity.INFO,
            conditions=[
                AlertCondition(
                    name="rejected_count_gt_zero",
                    field_path="rejected_count",
                    operator=AlertConditionOperator.GT,
                    threshold=0
                )
            ],
            route_target=AlertRouteTarget.LOG_ONLY,
            notification_type=NotificationType.RISK_DECISIONS,
            priority=NotificationPriority.NORMAL,
            cooldown_seconds=1800,
            suppress_duplicates=True,
            max_alerts_per_run=3
        )
    ]

def portfolio_alert_policies() -> List[AlertPolicy]:
    return [
        AlertPolicy(
            policy_id="portfolio_needs_review",
            name="Portfolio Needs Review",
            scope=AlertPolicyScope.PORTFOLIO,
            alert_type=AlertType.PORTFOLIO_BASKET_REVIEW,
            enabled=True,
            severity=AlertSeverity.WARNING,
            min_severity_to_route=AlertSeverity.INFO,
            conditions=[
                AlertCondition(
                    name="review_status_warning",
                    field_path="review_status",
                    operator=AlertConditionOperator.IN,
                    threshold=["NEEDS_REVIEW", "REJECTED", "needs_review", "rejected"]
                )
            ],
            route_target=AlertRouteTarget.LOG_ONLY,
            notification_type=NotificationType.PORTFOLIO_BASKET,
            priority=NotificationPriority.NORMAL,
            cooldown_seconds=3600,
            suppress_duplicates=True,
            max_alerts_per_run=2
        )
    ]

def runtime_alert_policies() -> List[AlertPolicy]:
    return [
        AlertPolicy(
            policy_id="runtime_error",
            name="Runtime Error",
            scope=AlertPolicyScope.RUNTIME,
            alert_type=AlertType.RUNTIME_ERROR,
            enabled=True,
            severity=AlertSeverity.CRITICAL,
            min_severity_to_route=AlertSeverity.INFO,
            conditions=[
                AlertCondition(
                    name="error_count_gt_zero",
                    field_path="error_count",
                    operator=AlertConditionOperator.GT,
                    threshold=0
                )
            ],
            route_target=AlertRouteTarget.LOG_ONLY,
            notification_type=NotificationType.RUNTIME_ERROR,
            priority=NotificationPriority.CRITICAL,
            cooldown_seconds=300,
            suppress_duplicates=True,
            max_alerts_per_run=5
        )
    ]

def health_alert_policies() -> List[AlertPolicy]:
    return [
        AlertPolicy(
            policy_id="health_error",
            name="Health Error",
            scope=AlertPolicyScope.HEALTH,
            alert_type=AlertType.HEALTH_ERROR,
            enabled=True,
            severity=AlertSeverity.HIGH,
            min_severity_to_route=AlertSeverity.INFO,
            conditions=[
                AlertCondition(
                    name="failed_checks_gt_zero",
                    field_path="failed_checks",
                    operator=AlertConditionOperator.GT,
                    threshold=0
                )
            ],
            route_target=AlertRouteTarget.LOG_ONLY,
            notification_type=NotificationType.HEALTH_SUMMARY,
            priority=NotificationPriority.HIGH,
            cooldown_seconds=300,
            suppress_duplicates=True,
            max_alerts_per_run=2
        )
    ]

def get_alert_policy_by_id(policies: List[AlertPolicy], policy_id: str) -> Optional[AlertPolicy]:
    for p in policies:
        if p.policy_id == policy_id:
            return p
    return None

def filter_enabled_alert_policies(policies: List[AlertPolicy], scope: Optional[AlertPolicyScope] = None) -> List[AlertPolicy]:
    filtered = []
    for p in policies:
        if not p.enabled:
            continue
        if scope and p.scope != scope:
            continue
        filtered.append(p)
    return filtered

def alert_policies_to_text(policies: List[AlertPolicy]) -> str:
    lines = []
    for p in policies:
        lines.append(f"Policy: {p.name} ({p.policy_id})")
        lines.append(f"  Scope: {p.scope.value if hasattr(p.scope, 'value') else p.scope}")
        lines.append(f"  Alert Type: {p.alert_type.value if hasattr(p.alert_type, 'value') else p.alert_type}")
        lines.append(f"  Severity: {p.severity.value if hasattr(p.severity, 'value') else p.severity}")
        lines.append(f"  Target: {p.route_target.value if hasattr(p.route_target, 'value') else p.route_target}")
    return "\n".join(lines)
