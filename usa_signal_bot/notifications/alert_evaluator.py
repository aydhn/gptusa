import datetime
from typing import List, Optional, Tuple

from usa_signal_bot.core.enums import AlertDecisionStatus, AlertSuppressionReason
from usa_signal_bot.notifications.alert_models import (
    AlertDecision,
    AlertEvaluationContext,
    AlertEvaluationResult,
    AlertPolicy,
    create_alert_decision_id,
    create_alert_evaluation_id
)
from usa_signal_bot.notifications.alert_conditions import (
    AlertConditionResult,
    evaluate_alert_conditions,
    all_required_conditions_passed,
    condition_results_to_dict
)
from usa_signal_bot.notifications.alert_routing import route_alert_decision, build_notification_from_alert_decision
from usa_signal_bot.notifications.alert_cooldown import AlertCooldownManager
from usa_signal_bot.notifications.notification_models import NotificationMessage

class AlertEvaluator:
    def __init__(self, policies: Optional[List[AlertPolicy]] = None, cooldown_manager: Optional[AlertCooldownManager] = None):
        self.policies = policies or []
        self.cooldown_manager = cooldown_manager or AlertCooldownManager()
        self.run_alert_counts = {}

    def evaluate(self, context: AlertEvaluationContext) -> AlertEvaluationResult:
        result = AlertEvaluationResult(
            evaluation_id=create_alert_evaluation_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            run_id=context.run_id,
            total_policies=len(self.policies),
            triggered_count=0,
            suppressed_count=0,
            routed_count=0,
            queued_count=0,
            decisions=[],
            messages=[],
            warnings=[],
            errors=[]
        )

        enabled_policies = [p for p in self.policies if p.enabled and (p.scope == context.scope)]
        if not enabled_policies:
            return result

        for policy in enabled_policies:
            try:
                decision = self.evaluate_policy(policy, context)
                result.decisions.append(decision)

                if decision.status == AlertDecisionStatus.ROUTED:
                    result.triggered_count += 1
                    result.routed_count += 1
                elif decision.status == AlertDecisionStatus.SUPPRESSED:
                    if decision.suppression_reason != AlertSuppressionReason.BELOW_THRESHOLD:
                        result.triggered_count += 1
                    result.suppressed_count += 1

            except Exception as e:
                result.errors.append(f"Error evaluating policy {policy.policy_id}: {str(e)}")

        return result

    def evaluate_policy(self, policy: AlertPolicy, context: AlertEvaluationContext) -> AlertDecision:
        condition_results = evaluate_alert_conditions(policy.conditions, context.payload)

        triggered = True
        if policy.conditions:
            triggered = all_required_conditions_passed(condition_results, policy.conditions)

        if not triggered:
            return self.build_decision(policy, context, condition_results, False, AlertSuppressionReason.BELOW_THRESHOLD)

        # Check max alerts per run
        run_count = self.run_alert_counts.get(policy.policy_id, 0)
        if run_count >= policy.max_alerts_per_run:
            return self.build_decision(policy, context, condition_results, True, AlertSuppressionReason.DUPLICATE) # Map over-limit to DUPLICATE for now

        # Check cooldown
        in_cooldown, _ = self.cooldown_manager.is_in_cooldown(policy, context.created_at_utc)
        if in_cooldown:
            return self.build_decision(policy, context, condition_results, True, AlertSuppressionReason.COOLDOWN_ACTIVE)

        # Build initial decision
        decision = self.build_decision(policy, context, condition_results, True)

        # Route
        routed, supp_reason, channel = route_alert_decision(policy, decision)
        if not routed:
            decision.status = AlertDecisionStatus.SUPPRESSED
            decision.suppression_reason = supp_reason
            return decision

        decision.status = AlertDecisionStatus.ROUTED
        self.cooldown_manager.remember(policy, context.created_at_utc)
        self.run_alert_counts[policy.policy_id] = run_count + 1

        return decision

    def build_decision(self, policy: AlertPolicy, context: AlertEvaluationContext, condition_results: List[AlertConditionResult], triggered: bool, suppression_reason: Optional[AlertSuppressionReason] = None) -> AlertDecision:
        status = AlertDecisionStatus.SUPPRESSED if not triggered or suppression_reason else AlertDecisionStatus.CREATED

        # Basic payload excerpt (avoid large payloads, sensitive data logic usually outside but we limit keys)
        excerpt = {k: v for k, v in context.payload.items() if k in ["run_id", "status", "error_count", "candidate_count"]}

        return AlertDecision(
            decision_id=create_alert_decision_id(policy.policy_id),
            policy_id=policy.policy_id,
            alert_type=policy.alert_type,
            severity=policy.severity,
            status=status,
            route_target=policy.route_target,
            notification_message_id=None,
            suppression_reason=suppression_reason,
            condition_results=condition_results_to_dict(condition_results),
            title=f"[{policy.severity.value if hasattr(policy.severity, 'value') else policy.severity}] {policy.name}",
            summary=f"Alert {policy.name} triggered for run {context.run_id}" if triggered else f"Alert {policy.name} did not trigger",
            payload_excerpt=excerpt,
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            warnings=[],
            errors=[]
        )

    def build_messages(self, result: AlertEvaluationResult) -> List[NotificationMessage]:
        messages = []
        policy_map = {p.policy_id: p for p in self.policies}

        for decision in result.decisions:
            if decision.status == AlertDecisionStatus.ROUTED:
                policy = policy_map.get(decision.policy_id)
                if policy:
                    msg = build_notification_from_alert_decision(policy, decision)
                    decision.notification_message_id = msg.message_id
                    decision.status = AlertDecisionStatus.QUEUED
                    messages.append(msg)
                    result.queued_count += 1
        return messages

    def evaluate_and_build_messages(self, context: AlertEvaluationContext) -> Tuple[AlertEvaluationResult, List[NotificationMessage]]:
        res = self.evaluate(context)
        msgs = self.build_messages(res)
        res.messages = msgs
        return res, msgs
