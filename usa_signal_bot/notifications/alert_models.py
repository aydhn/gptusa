import datetime
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    AlertConditionOperator,
    AlertDecisionStatus,
    AlertPolicyScope,
    AlertRouteTarget,
    AlertSeverity,
    AlertSuppressionReason,
    AlertType,
    NotificationType,
    NotificationPriority
)
from usa_signal_bot.notifications.notification_models import NotificationMessage, notification_message_to_dict

@dataclass
class AlertCondition:
    name: str
    field_path: str
    operator: AlertConditionOperator
    threshold: Any = None
    lower: Optional[float] = None
    upper: Optional[float] = None
    required: bool = True
    description: Optional[str] = None

@dataclass
class AlertPolicy:
    policy_id: str
    name: str
    scope: AlertPolicyScope
    alert_type: AlertType
    enabled: bool
    severity: AlertSeverity
    min_severity_to_route: AlertSeverity
    conditions: List[AlertCondition]
    route_target: AlertRouteTarget
    notification_type: NotificationType
    priority: NotificationPriority
    cooldown_seconds: int
    suppress_duplicates: bool
    max_alerts_per_run: int
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AlertEvaluationContext:
    payload: Dict[str, Any]
    run_id: Optional[str] = None
    scope: AlertPolicyScope = AlertPolicyScope.GLOBAL
    source_path: Optional[str] = None
    created_at_utc: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at_utc:
            self.created_at_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class AlertDecision:
    decision_id: str
    policy_id: str
    alert_type: AlertType
    severity: AlertSeverity
    status: AlertDecisionStatus
    route_target: AlertRouteTarget
    notification_message_id: Optional[str]
    suppression_reason: Optional[AlertSuppressionReason]
    condition_results: List[Dict[str, Any]]
    title: str
    summary: str
    payload_excerpt: Dict[str, Any]
    created_at_utc: str
    warnings: List[str]
    errors: List[str]

@dataclass
class AlertEvaluationResult:
    evaluation_id: str
    created_at_utc: str
    run_id: Optional[str]
    total_policies: int
    triggered_count: int
    suppressed_count: int
    routed_count: int
    queued_count: int
    decisions: List[AlertDecision]
    messages: List[NotificationMessage]
    warnings: List[str]
    errors: List[str]

def alert_condition_to_dict(condition: AlertCondition) -> Dict[str, Any]:
    return {
        "name": condition.name,
        "field_path": condition.field_path,
        "operator": condition.operator.value if hasattr(condition.operator, "value") else condition.operator,
        "threshold": condition.threshold,
        "lower": condition.lower,
        "upper": condition.upper,
        "required": condition.required,
        "description": condition.description
    }

def alert_policy_to_dict(policy: AlertPolicy) -> Dict[str, Any]:
    return {
        "policy_id": policy.policy_id,
        "name": policy.name,
        "scope": policy.scope.value if hasattr(policy.scope, "value") else policy.scope,
        "alert_type": policy.alert_type.value if hasattr(policy.alert_type, "value") else policy.alert_type,
        "enabled": policy.enabled,
        "severity": policy.severity.value if hasattr(policy.severity, "value") else policy.severity,
        "min_severity_to_route": policy.min_severity_to_route.value if hasattr(policy.min_severity_to_route, "value") else policy.min_severity_to_route,
        "conditions": [alert_condition_to_dict(c) for c in policy.conditions],
        "route_target": policy.route_target.value if hasattr(policy.route_target, "value") else policy.route_target,
        "notification_type": policy.notification_type.value if hasattr(policy.notification_type, "value") else policy.notification_type,
        "priority": policy.priority.value if hasattr(policy.priority, "value") else policy.priority,
        "cooldown_seconds": policy.cooldown_seconds,
        "suppress_duplicates": policy.suppress_duplicates,
        "max_alerts_per_run": policy.max_alerts_per_run,
        "metadata": policy.metadata
    }

def alert_evaluation_context_to_dict(context: AlertEvaluationContext) -> Dict[str, Any]:
    return {
        "run_id": context.run_id,
        "scope": context.scope.value if hasattr(context.scope, "value") else context.scope,
        "payload": context.payload,
        "source_path": context.source_path,
        "created_at_utc": context.created_at_utc,
        "metadata": context.metadata
    }

def alert_decision_to_dict(decision: AlertDecision) -> Dict[str, Any]:
    return {
        "decision_id": decision.decision_id,
        "policy_id": decision.policy_id,
        "alert_type": decision.alert_type.value if hasattr(decision.alert_type, "value") else decision.alert_type,
        "severity": decision.severity.value if hasattr(decision.severity, "value") else decision.severity,
        "status": decision.status.value if hasattr(decision.status, "value") else decision.status,
        "route_target": decision.route_target.value if hasattr(decision.route_target, "value") else decision.route_target,
        "notification_message_id": decision.notification_message_id,
        "suppression_reason": decision.suppression_reason.value if decision.suppression_reason and hasattr(decision.suppression_reason, "value") else decision.suppression_reason,
        "condition_results": decision.condition_results,
        "title": decision.title,
        "summary": decision.summary,
        "payload_excerpt": decision.payload_excerpt,
        "created_at_utc": decision.created_at_utc,
        "warnings": decision.warnings,
        "errors": decision.errors
    }

def alert_evaluation_result_to_dict(result: AlertEvaluationResult) -> Dict[str, Any]:
    return {
        "evaluation_id": result.evaluation_id,
        "created_at_utc": result.created_at_utc,
        "run_id": result.run_id,
        "total_policies": result.total_policies,
        "triggered_count": result.triggered_count,
        "suppressed_count": result.suppressed_count,
        "routed_count": result.routed_count,
        "queued_count": result.queued_count,
        "decisions": [alert_decision_to_dict(d) for d in result.decisions],
        "messages": [notification_message_to_dict(m) for m in result.messages],
        "warnings": result.warnings,
        "errors": result.errors
    }

def validate_alert_condition(condition: AlertCondition) -> None:
    if not condition.name:
        raise ValueError("AlertCondition name cannot be empty")
    if not condition.field_path:
        raise ValueError("AlertCondition field_path cannot be empty")
    if condition.operator == AlertConditionOperator.BETWEEN and (condition.lower is None or condition.upper is None):
        raise ValueError("AlertCondition operator BETWEEN requires lower and upper bounds")

def validate_alert_policy(policy: AlertPolicy) -> None:
    if not policy.policy_id:
        raise ValueError("AlertPolicy policy_id cannot be empty")
    if not policy.name:
        raise ValueError("AlertPolicy name cannot be empty")
    if policy.cooldown_seconds < 0:
        raise ValueError("AlertPolicy cooldown_seconds cannot be negative")
    if policy.max_alerts_per_run <= 0:
        raise ValueError("AlertPolicy max_alerts_per_run must be positive")
    for c in policy.conditions:
        validate_alert_condition(c)

def validate_alert_evaluation_context(context: AlertEvaluationContext) -> None:
    if context.payload is None:
        raise ValueError("AlertEvaluationContext payload cannot be None")

def create_alert_policy_id(name: str) -> str:
    from usa_signal_bot.utils.text_utils import snake_case
    return f"policy_{snake_case(name)}_{uuid.uuid4().hex[:6]}"

def create_alert_decision_id(policy_id: str) -> str:
    return f"dec_{policy_id}_{uuid.uuid4().hex[:8]}"

def create_alert_evaluation_id(prefix: str = "alert_eval") -> str:
    return f"{prefix}_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
