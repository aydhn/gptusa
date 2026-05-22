
from typing import Any, List, Optional
import datetime
from usa_signal_bot.core.enums import (
    ActivationAttemptType, ActivationFirewallDecision, ActivationFirewallStatus, PaperReadinessBoardRiskFlag
)
from usa_signal_bot.paper_readiness_board.readiness_board_models import (
    ActivationFirewallRule, ActivationFirewallEvent, create_activation_firewall_rule_id, create_activation_firewall_event_id
)

def dangerous_activation_attempt_types() -> List[ActivationAttemptType]:
    return [
        ActivationAttemptType.ENABLE_ACTIVE_PAPER,
        ActivationAttemptType.ENABLE_CANDIDATE_STRATEGY,
        ActivationAttemptType.PATCH_PAPER_CONFIG,
        ActivationAttemptType.COMMIT_PAPER_STATE,
        ActivationAttemptType.CREATE_PAPER_ORDER,
        ActivationAttemptType.SEND_BROKER_ORDER,
        ActivationAttemptType.SEND_TELEGRAM_REAL,
        ActivationAttemptType.UNLOCK_ARCHIVE,
        ActivationAttemptType.UNLOCK_FINAL_LOCK
    ]

def rule_for_activation_attempt(attempt_type: ActivationAttemptType) -> ActivationFirewallRule:
    return ActivationFirewallRule(
        rule_id=create_activation_firewall_rule_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        attempt_type=attempt_type,
        enabled=True,
        blocking=True,
        decision=ActivationFirewallDecision.DENY_ACTIVATION,
        description=f"Rule to deny {attempt_type.value}",
        risk_flags=[], warnings=[], errors=[]
    )

def default_activation_firewall_rules() -> List[ActivationFirewallRule]:
    return [rule_for_activation_attempt(a) for a in dangerous_activation_attempt_types()]

def validate_activation_firewall_rules_complete(rules: List[ActivationFirewallRule]) -> List[str]:
    covered = set(r.attempt_type for r in rules if r.enabled and r.blocking)
    dangerous = set(dangerous_activation_attempt_types())
    missing = dangerous - covered
    return [f"Missing rule for {m.value}" for m in missing]

def activation_firewall_rules_summary(rules: List[ActivationFirewallRule]) -> dict:
    return {"rule_count": len(rules), "covered_types": [r.attempt_type.value for r in rules]}

def activation_firewall_rules_to_text(rules: List[ActivationFirewallRule], limit: int = 100) -> str:
    return "\n".join([f"{r.attempt_type.value}: {r.decision.value}" for r in rules[:limit]])

class FinalActivationFirewall:
    def __init__(self, rules: List[ActivationFirewallRule] = None):
        self.rules = rules or default_activation_firewall_rules()

    def evaluate_attempt(self, attempt_type: ActivationAttemptType, payload: dict = None, source_component: str = None) -> ActivationFirewallEvent:
        return self.deny_activation_attempt(attempt_type, payload, source_component)

    def activation_allowed(self, attempt_type: ActivationAttemptType) -> bool:
        return False

    def deny_activation_attempt(self, attempt_type: ActivationAttemptType, payload: dict = None, source_component: str = None) -> ActivationFirewallEvent:
        return ActivationFirewallEvent(
            event_id=create_activation_firewall_event_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            attempt_type=attempt_type,
            status=ActivationFirewallStatus.ACTIVATION_DENIED,
            decision=ActivationFirewallDecision.DENY_ACTIVATION,
            blocked=True,
            activation_allowed=False,
            source_component=source_component,
            description=f"Activation denied for {attempt_type.value}",
            payload_summary={"payload_size": len(str(payload))} if payload else {},
            risk_flags=[], warnings=[], errors=[]
        )

    def validate_firewall_enabled(self) -> List[str]:
        if not self.rules:
            return ["Firewall has no rules."]
        return validate_activation_firewall_rules_complete(self.rules)

    def firewall_summary(self, events: List[ActivationFirewallEvent]) -> dict:
        return {
            "events_evaluated": len(events),
            "all_blocked": all(e.blocked for e in events)
        }

def simulate_activation_attempts(firewall: FinalActivationFirewall = None) -> List[ActivationFirewallEvent]:
    fw = firewall or FinalActivationFirewall()
    return [
        fw.evaluate_attempt(ActivationAttemptType.ENABLE_ACTIVE_PAPER),
        fw.evaluate_attempt(ActivationAttemptType.CREATE_PAPER_ORDER),
        fw.evaluate_attempt(ActivationAttemptType.PATCH_PAPER_CONFIG)
    ]

def simulate_enable_active_paper_attempt(firewall: FinalActivationFirewall = None) -> ActivationFirewallEvent:
    return (firewall or FinalActivationFirewall()).evaluate_attempt(ActivationAttemptType.ENABLE_ACTIVE_PAPER)

def simulate_candidate_strategy_enable_attempt(firewall: FinalActivationFirewall = None) -> ActivationFirewallEvent:
    return (firewall or FinalActivationFirewall()).evaluate_attempt(ActivationAttemptType.ENABLE_CANDIDATE_STRATEGY)

def simulate_paper_config_patch_attempt(firewall: FinalActivationFirewall = None) -> ActivationFirewallEvent:
    return (firewall or FinalActivationFirewall()).evaluate_attempt(ActivationAttemptType.PATCH_PAPER_CONFIG)

def simulate_commit_paper_state_attempt(firewall: FinalActivationFirewall = None) -> ActivationFirewallEvent:
    return (firewall or FinalActivationFirewall()).evaluate_attempt(ActivationAttemptType.COMMIT_PAPER_STATE)

def simulate_create_paper_order_attempt(firewall: FinalActivationFirewall = None) -> ActivationFirewallEvent:
    return (firewall or FinalActivationFirewall()).evaluate_attempt(ActivationAttemptType.CREATE_PAPER_ORDER)

def activation_attempt_simulator_summary(events: List[ActivationFirewallEvent]) -> dict:
    return {"simulated_events": len(events), "all_blocked": all(e.blocked for e in events)}

def activation_attempt_simulator_to_text(events: List[ActivationFirewallEvent]) -> str:
    return "\n".join([f"{e.attempt_type.value}: blocked={e.blocked}" for e in events])
