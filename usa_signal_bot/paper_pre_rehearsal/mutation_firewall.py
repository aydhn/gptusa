from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    MutationFirewallRule,
    MutationFirewallEvent,
    create_mutation_firewall_event_id,
    validate_mutation_firewall_event
)
from usa_signal_bot.paper_pre_rehearsal.firewall_rules import default_mutation_firewall_rules, rule_for_attempt_type
from usa_signal_bot.core.enums import MutationAttemptType, FirewallAction

class PaperStateMutationFirewall:
    def __init__(self, rules: Optional[List[MutationFirewallRule]] = None):
        self.rules = rules or default_mutation_firewall_rules()
        self._rules_by_type = {r.attempt_type: r for r in self.rules}

    def _get_rule(self, attempt_type: MutationAttemptType) -> MutationFirewallRule:
        if attempt_type in self._rules_by_type:
            return self._rules_by_type[attempt_type]
        return rule_for_attempt_type(attempt_type)

    def is_attempt_allowed(self, attempt_type: MutationAttemptType) -> bool:
        rule = self._get_rule(attempt_type)
        return not rule.blocking or rule.action == FirewallAction.ALLOW_READ_ONLY

    def is_attempt_blocking(self, attempt_type: MutationAttemptType) -> bool:
        rule = self._get_rule(attempt_type)
        return rule.blocking and rule.action in [FirewallAction.BLOCK_SESSION, FirewallAction.DENY_AND_RECORD]

    def evaluate_attempt(self, attempt_type: MutationAttemptType, session_id: Optional[str] = None, source_component: Optional[str] = None, payload: Optional[Dict[str, Any]] = None) -> MutationFirewallEvent:
        rule = self._get_rule(attempt_type)
        blocked = rule.blocking and rule.action in [FirewallAction.BLOCK_SESSION, FirewallAction.DENY_AND_RECORD]

        event = MutationFirewallEvent(
            event_id=create_mutation_firewall_event_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            attempt_type=attempt_type,
            action=rule.action,
            blocked=blocked,
            session_id=session_id,
            source_component=source_component,
            description=f"Evaluated {attempt_type.value} attempt. Blocked: {blocked}",
            risk_flags=rule.risk_flags.copy(),
            payload_summary={"payload_provided": payload is not None},
            warnings=[],
            errors=[]
        )
        validate_mutation_firewall_event(event)
        return event

    def record_denied_attempt(self, attempt_type: MutationAttemptType, session_id: Optional[str] = None, source_component: Optional[str] = None, payload: Optional[Dict[str, Any]] = None) -> MutationFirewallEvent:
        return self.evaluate_attempt(attempt_type, session_id, source_component, payload)

    def firewall_summary(self, events: List[MutationFirewallEvent]) -> Dict[str, Any]:
        return {
            "total_events": len(events),
            "blocked_events": sum(1 for e in events if e.blocked),
            "allowed_events": sum(1 for e in events if not e.blocked)
        }
