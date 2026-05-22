from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationQueueItem,
    HumanReviewBundle
)
from usa_signal_bot.core.enums import ActivationStillDeniedDecision, ReadinessConfirmationRiskFlag
from usa_signal_bot.paper_readiness_confirmation.readiness_confidence import readiness_confidence_blocks

def determine_confirmation_decision(
    queue_item: ReadinessConfirmationQueueItem,
    bundle: HumanReviewBundle | None = None
) -> ActivationStillDeniedDecision:

    if readiness_confidence_blocks(queue_item.safety_flags):
        return ActivationStillDeniedDecision.BLOCK

    if not bundle:
        return ActivationStillDeniedDecision.REQUEST_MANUAL_REVIEW

    if ReadinessConfirmationRiskFlag.EVIDENCE_MISSING in queue_item.safety_flags or ReadinessConfirmationRiskFlag.EVIDENCE_STALE in queue_item.safety_flags:
         return ActivationStillDeniedDecision.REQUEST_EVIDENCE_REFRESH

    return ActivationStillDeniedDecision.KEEP_ACTIVATION_DENIED_AND_QUEUE_HUMAN_REVIEW

def confirmation_decision_reasons(decision: ActivationStillDeniedDecision, flags: list[ReadinessConfirmationRiskFlag]) -> list[str]:
    reasons = []
    if decision == ActivationStillDeniedDecision.BLOCK:
         reasons.append("Safety flags blocking")
    if decision == ActivationStillDeniedDecision.REQUEST_MANUAL_REVIEW:
         reasons.append("Bundle missing")
    if decision == ActivationStillDeniedDecision.REQUEST_EVIDENCE_REFRESH:
         reasons.append("Evidence missing or stale")
    if decision == ActivationStillDeniedDecision.KEEP_ACTIVATION_DENIED_AND_QUEUE_HUMAN_REVIEW:
         reasons.append("All checks passed, ready for review")
    return reasons

def confirmation_decision_followups(decision: ActivationStillDeniedDecision, flags: list[ReadinessConfirmationRiskFlag]) -> list[str]:
    followups = []
    if decision == ActivationStillDeniedDecision.REQUEST_EVIDENCE_REFRESH:
         followups.append("Run evidence refresh")
    if decision == ActivationStillDeniedDecision.REQUEST_MANUAL_REVIEW:
         followups.append("Create human review bundle")
    return followups

def confirmation_decision_allows_activation(decision: ActivationStillDeniedDecision) -> bool:
    return False

def confirmation_decision_to_text(payload: dict[str, Any]) -> str:
    return "Decision Metadata Evaluated"
