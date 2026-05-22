import datetime
from typing import Any, Dict, List
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    MutationFirewallRule,
    create_mutation_firewall_rule_id,
    validate_mutation_firewall_rule
)
from usa_signal_bot.core.enums import MutationAttemptType, FirewallAction, PrePaperRiskFlag

def dangerous_mutation_attempt_types() -> List[MutationAttemptType]:
    return [
        MutationAttemptType.PAPER_STATE_WRITE,
        MutationAttemptType.PAPER_ORDER_CREATE,
        MutationAttemptType.PAPER_POSITION_MUTATION,
        MutationAttemptType.PAPER_PORTFOLIO_MUTATION,
        MutationAttemptType.PAPER_CASH_MUTATION,
        MutationAttemptType.PAPER_EQUITY_MUTATION,
        MutationAttemptType.PAPER_FILL_CREATE,
        MutationAttemptType.BROKER_ORDER_SEND,
        MutationAttemptType.TELEGRAM_REAL_SEND,
        MutationAttemptType.PRODUCTION_CONFIG_PATCH,
        MutationAttemptType.ACTIVE_PAPER_ENABLE,
        MutationAttemptType.OBSERVER_UNLOCK,
        MutationAttemptType.ARCHIVE_UNLOCK,
        MutationAttemptType.FINAL_LOCK_UNLOCK
    ]

def rule_for_attempt_type(attempt_type: MutationAttemptType) -> MutationFirewallRule:
    risk_flags = []

    # Map attempt type to risk flags
    if "BROKER" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.BROKER_ORDER_RISK)
    elif "PAPER_ORDER" in attempt_type.value or "PAPER_FILL" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.PAPER_ORDER_RISK)
    elif "PAPER_STATE" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.PAPER_STATE_MUTATION_RISK)
    elif "PORTFOLIO" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.PAPER_PORTFOLIO_MUTATION_RISK)
    elif "CASH" in attempt_type.value or "EQUITY" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.PAPER_CASH_MUTATION_RISK)
    elif "POSITION" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.PAPER_POSITION_MUTATION_RISK)
    elif "TELEGRAM" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.TELEGRAM_REAL_SEND_RISK)
    elif "CONFIG" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    elif "ENABLE" in attempt_type.value or "UNLOCK" in attempt_type.value:
        risk_flags.append(PrePaperRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if "ARCHIVE" in attempt_type.value:
            risk_flags.append(PrePaperRiskFlag.ARCHIVE_UNLOCK_RISK)
        if "FINAL_LOCK" in attempt_type.value:
            risk_flags.append(PrePaperRiskFlag.FINAL_LOCK_UNLOCK_RISK)

    action = FirewallAction.BLOCK_SESSION if attempt_type in dangerous_mutation_attempt_types() else FirewallAction.DENY_AND_RECORD
    if attempt_type == MutationAttemptType.UNKNOWN:
        action = FirewallAction.DENY_AND_RECORD

    rule = MutationFirewallRule(


        attempt_type=attempt_type,
        action=action,
        enabled=True,
        blocking=True,
        description=f"Block {attempt_type.value} attempts during pre-paper rehearsal",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )
    validate_mutation_firewall_rule(rule)
    return rule

def default_mutation_firewall_rules() -> List[MutationFirewallRule]:
    return [rule_for_attempt_type(at) for at in dangerous_mutation_attempt_types()]

def validate_firewall_rules_complete(rules: List[MutationFirewallRule]) -> List[str]:
    violations = []
    covered_types = {r.attempt_type for r in rules}
    for at in dangerous_mutation_attempt_types():
        if at not in covered_types:
            violations.append(f"Missing firewall rule for dangerous attempt type: {at.value}")
    return violations

def firewall_rules_summary(rules: List[MutationFirewallRule]) -> Dict[str, Any]:
    return {
        "rule_count": len(rules),
        "complete": len(validate_firewall_rules_complete(rules)) == 0,
        "blocked_types": [r.attempt_type.value for r in rules if r.blocking]
    }

def firewall_rules_to_text(rules: List[MutationFirewallRule], limit: int = 100) -> str:
    s = firewall_rules_summary(rules)
    return f"Firewall Rules: {s['rule_count']} total, Complete: {s['complete']}"
