from typing import Any
from usa_signal_bot.core.enums import ReadinessConfidenceLevel, ReadinessConfirmationRiskFlag
from usa_signal_bot.paper_readiness_confirmation.eligibility_checker import readiness_confirmation_safety_flags_from_firewall_audit

def calculate_readiness_confidence(firewall_audit_payload: dict[str, Any]) -> ReadinessConfidenceLevel:
    if not firewall_audit_payload:
        return ReadinessConfidenceLevel.INSUFFICIENT_DATA

    flags = readiness_confirmation_safety_flags_from_firewall_audit(firewall_audit_payload)
    if readiness_confidence_blocks(flags):
        return ReadinessConfidenceLevel.BLOCKED

    reasons = readiness_confidence_reasons(firewall_audit_payload)
    if "Missing critical audit" in reasons:
        return ReadinessConfidenceLevel.INSUFFICIENT_DATA
    if "Evidence partial/stale" in reasons:
        return ReadinessConfidenceLevel.MEDIUM

    return ReadinessConfidenceLevel.HIGH

def readiness_confidence_score(firewall_audit_payload: dict[str, Any]) -> float | None:
    level = calculate_readiness_confidence(firewall_audit_payload)
    mapping = {
        ReadinessConfidenceLevel.HIGH: 1.0,
        ReadinessConfidenceLevel.MEDIUM: 0.5,
        ReadinessConfidenceLevel.LOW: 0.2,
        ReadinessConfidenceLevel.INSUFFICIENT_DATA: 0.0,
        ReadinessConfidenceLevel.BLOCKED: 0.0,
        ReadinessConfidenceLevel.UNKNOWN: 0.0,
    }
    return mapping.get(level, 0.0)

def readiness_confidence_reasons(firewall_audit_payload: dict[str, Any]) -> list[str]:
    reasons = []

    if not firewall_audit_payload.get("zero_mutation_audit"):
         reasons.append("Missing critical audit")
    if not firewall_audit_payload.get("firewall_replay_result"):
         reasons.append("Missing critical audit")

    if firewall_audit_payload.get("pre_paper_evidence_refresh", {}).get("status") != "FRESH":
         reasons.append("Evidence partial/stale")

    return reasons

def readiness_confidence_blocks(flags: list[ReadinessConfirmationRiskFlag]) -> bool:
    blocking_flags = [
        ReadinessConfirmationRiskFlag.REAL_ORDER_RISK,
        ReadinessConfirmationRiskFlag.PAPER_ORDER_RISK,
        ReadinessConfirmationRiskFlag.BROKER_ORDER_RISK,
        ReadinessConfirmationRiskFlag.PAPER_STATE_MUTATION_RISK,
        ReadinessConfirmationRiskFlag.TELEGRAM_REAL_SEND_RISK,
        ReadinessConfirmationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        ReadinessConfirmationRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK
    ]
    return any(f in flags for f in blocking_flags)

def readiness_confidence_to_text(payload: dict[str, Any]) -> str:
    level = calculate_readiness_confidence(payload)
    return f"Confidence Level: {level.value}"
