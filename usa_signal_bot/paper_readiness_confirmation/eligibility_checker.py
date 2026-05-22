from typing import Any
from usa_signal_bot.core.enums import ReadinessConfirmationDecision, ReadinessConfirmationRiskFlag, ReadinessConfirmationQueueStatus
from usa_signal_bot.paper_readiness_confirmation.firewall_audit_ingestion import firewall_audit_supports_readiness_confirmation

def evaluate_readiness_confirmation_eligibility(firewall_audit_payload: dict[str, Any]) -> ReadinessConfirmationDecision:
    reasons = readiness_confirmation_eligibility_reasons(firewall_audit_payload)
    if "Missing firewall audit" in reasons:
        return ReadinessConfirmationDecision.REQUEST_FIREWALL_AUDIT_REFRESH
    if "Zero mutation issue" in reasons:
        return ReadinessConfirmationDecision.REQUEST_ZERO_MUTATION_RETEST
    if "Evidence missing/stale" in reasons:
        return ReadinessConfirmationDecision.REQUEST_EVIDENCE_REFRESH
    if "Block flags" in reasons:
        return ReadinessConfirmationDecision.BLOCK

    supports, _ = firewall_audit_supports_readiness_confirmation(firewall_audit_payload)
    if supports:
        return ReadinessConfirmationDecision.QUEUE_FOR_HUMAN_REVIEW
    return ReadinessConfirmationDecision.INCONCLUSIVE

def readiness_confirmation_eligibility_reasons(firewall_audit_payload: dict[str, Any]) -> list[str]:
    reasons = []
    if not firewall_audit_payload:
        reasons.append("Missing firewall audit")
    else:
        flags = readiness_confirmation_safety_flags_from_firewall_audit(firewall_audit_payload)
        if ReadinessConfirmationRiskFlag.PAPER_STATE_MUTATION_RISK in flags:
            reasons.append("Zero mutation issue")
        if ReadinessConfirmationRiskFlag.EVIDENCE_MISSING in flags or ReadinessConfirmationRiskFlag.EVIDENCE_STALE in flags:
            reasons.append("Evidence missing/stale")
        if any(f in flags for f in [
            ReadinessConfirmationRiskFlag.REAL_ORDER_RISK,
            ReadinessConfirmationRiskFlag.PAPER_ORDER_RISK,
            ReadinessConfirmationRiskFlag.BROKER_ORDER_RISK,
            ReadinessConfirmationRiskFlag.TELEGRAM_REAL_SEND_RISK,
            ReadinessConfirmationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
            ReadinessConfirmationRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
            ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK
        ]):
            reasons.append("Block flags")
    return reasons

def readiness_confirmation_safety_flags_from_firewall_audit(payload: dict[str, Any]) -> list[ReadinessConfirmationRiskFlag]:
    flags = []
    if payload.get("activation_allowed"):
        flags.append(ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("allows_broker_execution"):
        flags.append(ReadinessConfirmationRiskFlag.BROKER_ORDER_RISK)
    if payload.get("allows_paper_state_mutation"):
        flags.append(ReadinessConfirmationRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("allows_config_patch"):
        flags.append(ReadinessConfirmationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if payload.get("allows_telegram_real_send"):
        flags.append(ReadinessConfirmationRiskFlag.TELEGRAM_REAL_SEND_RISK)

    zero_audit = payload.get("zero_mutation_audit", {})
    if zero_audit and zero_audit.get("status") == "FAILED":
         flags.append(ReadinessConfirmationRiskFlag.PAPER_STATE_MUTATION_RISK)

    return flags

def readiness_confirmation_status_from_decision(decision: ReadinessConfirmationDecision) -> ReadinessConfirmationQueueStatus:
    if decision == ReadinessConfirmationDecision.QUEUE_FOR_HUMAN_REVIEW:
        return ReadinessConfirmationQueueStatus.QUEUED
    if decision in [ReadinessConfirmationDecision.REJECT, ReadinessConfirmationDecision.BLOCK]:
        return ReadinessConfirmationQueueStatus.BLOCKED
    return ReadinessConfirmationQueueStatus.DRAFT

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_readiness_confirmation_eligibility(payload)
    reasons = readiness_confirmation_eligibility_reasons(payload)
    return f"Decision: {decision.value}\nReasons: {reasons}"
