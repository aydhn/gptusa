from typing import Any, Dict, List
from usa_signal_bot.core.enums import ReadinessRehearsalDecision, ReadinessRehearsalStatus, ReadinessRehearsalRiskFlag
from usa_signal_bot.paper_readiness_rehearsal.promotion_dossier_ingestion import (
    extract_safety_board_decision, extract_readiness_package
)

def evaluate_readiness_rehearsal_eligibility(promotion_payload: Dict[str, Any]) -> ReadinessRehearsalDecision:
    decision = extract_safety_board_decision(promotion_payload)
    pkg = extract_readiness_package(promotion_payload)

    if decision in ["BLOCK", "BLOCK_DOSSIER"]:
        return ReadinessRehearsalDecision.BLOCK
    if decision in ["REJECT", "REJECT_DOSSIER"]:
        return ReadinessRehearsalDecision.REJECT

    if not decision or decision == "DRAFT" or decision == "REVIEWING":
        return ReadinessRehearsalDecision.REQUEST_SAFETY_BOARD_REVIEW

    if decision == "REQUEST_MORE_EVIDENCE":
        return ReadinessRehearsalDecision.REQUEST_EVIDENCE_REFRESH

    if decision == "REQUEST_MANUAL_REVIEW":
        return ReadinessRehearsalDecision.REQUEST_MANUAL_REVIEW

    if decision == "PASS_FOR_STAGED_NON_EXECUTING_READINESS_PACKAGE":
        if pkg:
            return ReadinessRehearsalDecision.RUN_STAGED_REHEARSAL
        else:
            return ReadinessRehearsalDecision.REQUEST_PACKAGE_REFRESH

    return ReadinessRehearsalDecision.INCONCLUSIVE

def readiness_rehearsal_eligibility_reasons(promotion_payload: Dict[str, Any]) -> List[str]:
    decision = evaluate_readiness_rehearsal_eligibility(promotion_payload)
    return [f"Decision reached: {decision.value}"]

def readiness_rehearsal_safety_flags_from_promotion(payload: Dict[str, Any]) -> List[ReadinessRehearsalRiskFlag]:
    flags = []
    # Mocking extraction of safety flags from dossier payload
    return flags

def readiness_rehearsal_status_from_decision(decision: ReadinessRehearsalDecision) -> ReadinessRehearsalStatus:
    if decision == ReadinessRehearsalDecision.RUN_STAGED_REHEARSAL:
        return ReadinessRehearsalStatus.READY
    if decision in [ReadinessRehearsalDecision.BLOCK, ReadinessRehearsalDecision.REJECT]:
        return ReadinessRehearsalStatus.BLOCKED
    return ReadinessRehearsalStatus.DRAFT

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    decision = evaluate_readiness_rehearsal_eligibility(payload)
    return f"Readiness Rehearsal Eligibility: {decision.value}"
