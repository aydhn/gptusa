from typing import Any, List, Optional
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import FirewallReplayResult, ZeroMutationAuditReport, ReadinessAuditCheckpoint
from usa_signal_bot.core.enums import FirewallAuditRiskFlag

def collect_firewall_audit_safety_flags(replay_result: Optional[FirewallReplayResult] = None, zero_mutation_audit: Optional[ZeroMutationAuditReport] = None, checkpoint: Optional[ReadinessAuditCheckpoint] = None) -> List[FirewallAuditRiskFlag]:
    flags = []
    if replay_result: flags.extend(replay_result.risk_flags)
    if zero_mutation_audit: flags.extend(zero_mutation_audit.risk_flags)
    if checkpoint: flags.extend(checkpoint.risk_flags)
    return list(set(flags))

def firewall_audit_has_blocking_flags(flags: List[FirewallAuditRiskFlag]) -> bool:
    blocking = [
        FirewallAuditRiskFlag.REAL_ORDER_RISK,
        FirewallAuditRiskFlag.PAPER_ORDER_RISK,
        FirewallAuditRiskFlag.BROKER_ORDER_RISK,
        FirewallAuditRiskFlag.PAPER_STATE_MUTATION_RISK,
        FirewallAuditRiskFlag.TELEGRAM_REAL_SEND_RISK,
        FirewallAuditRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        FirewallAuditRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        FirewallAuditRiskFlag.FIREWALL_BYPASS_RISK,
        FirewallAuditRiskFlag.ZERO_MUTATION_FAILED,
        FirewallAuditRiskFlag.ACTIVATION_ALLOWED_RISK
    ]
    return any(f in blocking for f in flags)

def validate_firewall_audit_safety(replay_result: Optional[FirewallReplayResult] = None, zero_mutation_audit: Optional[ZeroMutationAuditReport] = None, checkpoint: Optional[ReadinessAuditCheckpoint] = None) -> List[str]:
    flags = collect_firewall_audit_safety_flags(replay_result, zero_mutation_audit, checkpoint)
    if firewall_audit_has_blocking_flags(flags):
        return [f"Safety check failed: {f.value}" for f in flags if f in flags] # simplified
    return []

def firewall_audit_safety_summary(flags: List[FirewallAuditRiskFlag]) -> dict[str, Any]:
    return {"blocked": firewall_audit_has_blocking_flags(flags), "flag_count": len(flags)}

def audit_safety_validator_to_text(payload: dict[str, Any]) -> str:
    return f"Safety blocked: {payload.get('blocked')}"
