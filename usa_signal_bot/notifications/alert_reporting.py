import json
from pathlib import Path
from typing import Any, Dict, List

from usa_signal_bot.notifications.alert_models import AlertDecision, AlertEvaluationResult, AlertPolicy
from usa_signal_bot.storage.json_store import write_json

def alert_policy_to_text(policy: AlertPolicy) -> str:
    lines = [
        f"Policy ID: {policy.policy_id}",
        f"Name: {policy.name}",
        f"Scope: {policy.scope.value if hasattr(policy.scope, 'value') else policy.scope}",
        f"Type: {policy.alert_type.value if hasattr(policy.alert_type, 'value') else policy.alert_type}",
        f"Severity: {policy.severity.value if hasattr(policy.severity, 'value') else policy.severity} (Min Route: {policy.min_severity_to_route.value if hasattr(policy.min_severity_to_route, 'value') else policy.min_severity_to_route})",
        f"Target: {policy.route_target.value if hasattr(policy.route_target, 'value') else policy.route_target}",
        f"Cooldown: {policy.cooldown_seconds}s",
        f"Max Alerts/Run: {policy.max_alerts_per_run}"
    ]
    if policy.conditions:
        lines.append("Conditions:")
        for c in policy.conditions:
            op = c.operator.value if hasattr(c.operator, 'value') else c.operator
            lines.append(f"  - {c.name}: {c.field_path} {op} {c.threshold}")
    return "\n".join(lines)

def alert_decision_to_text(decision: AlertDecision) -> str:
    lines = [
        f"Decision ID: {decision.decision_id}",
        f"Policy: {decision.policy_id}",
        f"Status: {decision.status.value if hasattr(decision.status, 'value') else decision.status}",
        f"Severity: {decision.severity.value if hasattr(decision.severity, 'value') else decision.severity}"
    ]
    if decision.suppression_reason:
        lines.append(f"Suppressed: {decision.suppression_reason.value if hasattr(decision.suppression_reason, 'value') else decision.suppression_reason}")
    if decision.notification_message_id:
        lines.append(f"Message ID: {decision.notification_message_id}")

    lines.append(f"Summary: {decision.summary}")
    return "\n".join(lines)

def alert_evaluation_result_to_text(result: AlertEvaluationResult, limit: int = 30) -> str:
    lines = [
        "--- ALERT EVALUATION SUMMARY ---",
        f"Evaluation ID: {result.evaluation_id}",
        f"Run ID: {result.run_id}",
        f"Total Policies: {result.total_policies}",
        f"Triggered: {result.triggered_count}",
        f"Suppressed: {result.suppressed_count}",
        f"Routed: {result.routed_count}",
        f"Queued Messages: {result.queued_count}"
    ]

    if result.errors:
        lines.append(f"Errors: {len(result.errors)}")
        for e in result.errors[:5]:
            lines.append(f"  - {e}")

    if result.decisions:
        lines.append("\nDecisions:")
        for d in result.decisions[:limit]:
            lines.append(alert_decision_to_text(d))
            lines.append("-" * 20)

    return "\n".join(lines)

def alert_policy_summary_to_text(policies: List[AlertPolicy]) -> str:
    lines = ["--- ALERT POLICIES ---"]
    for p in policies:
        lines.append(f"[{p.scope.value if hasattr(p.scope, 'value') else p.scope}] {p.name} ({p.severity.value if hasattr(p.severity, 'value') else p.severity}) -> {p.route_target.value if hasattr(p.route_target, 'value') else p.route_target}")
    return "\n".join(lines)

def alert_store_summary_to_text(summary: Dict[str, Any]) -> str:
    lines = [
        "--- ALERT STORE ---",
        f"Total Evaluations: {summary.get('total_evaluations', 0)}",
        f"Latest: {summary.get('latest', 'None')}"
    ]
    return "\n".join(lines)

def alert_limitations_text() -> str:
    return """
--- ALERT SYSTEM LIMITATIONS ---
1. Alerts are informational only and do not constitute investment advice.
2. The Alert Policy Layer will NEVER create, route, or execute live/paper broker orders.
3. Telegram real sending is disabled by default for safety.
4. Cooldown and Duplicate Suppression are basic protections, not guarantees against message floods.
""".strip()

def write_alert_report_json(path: Path, result: AlertEvaluationResult) -> Path:
    from usa_signal_bot.notifications.alert_models import alert_evaluation_result_to_dict
    write_json(path, alert_evaluation_result_to_dict(result))
    return path
