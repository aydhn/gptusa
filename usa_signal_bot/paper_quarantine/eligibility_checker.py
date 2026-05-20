from typing import Any

from usa_signal_bot.core.enums import (
    QuarantineEnrollmentDecision,
    QuarantineCandidateStatus,
    QuarantineSafetyFlag
)
from usa_signal_bot.paper_quarantine.shadow_governance_ingestion import (
    extract_shadow_governance_decision,
    extract_shadow_acceptance_score,
    extract_shadow_risk_flags,
)

def quarantine_safety_flags_from_shadow_governance(payload: dict[str, Any]) -> list[QuarantineSafetyFlag]:
    shadow_flags = extract_shadow_risk_flags(payload)
    flags = []

    if "high_risk" in shadow_flags or "block" in shadow_flags:
        flags.append(QuarantineSafetyFlag.BLOCKED_SHADOW_DECISION)

    decision = extract_shadow_governance_decision(payload)
    if decision in ["BLOCK"]:
        flags.append(QuarantineSafetyFlag.BLOCKED_SHADOW_DECISION)

    score = extract_shadow_acceptance_score(payload)
    if score is not None and score < 70.0:
        flags.append(QuarantineSafetyFlag.LOW_SHADOW_ACCEPTANCE_SCORE)

    if not decision:
        flags.append(QuarantineSafetyFlag.MISSING_SHADOW_GOVERNANCE)

    return list(set(flags))

def evaluate_quarantine_eligibility(shadow_governance_payload: dict[str, Any], min_score: float = 70.0) -> QuarantineEnrollmentDecision:
    decision = extract_shadow_governance_decision(shadow_governance_payload)
    score = extract_shadow_acceptance_score(shadow_governance_payload)
    safety_flags = quarantine_safety_flags_from_shadow_governance(shadow_governance_payload)

    if QuarantineSafetyFlag.BLOCKED_SHADOW_DECISION in safety_flags or decision in ["BLOCK"]:
        return QuarantineEnrollmentDecision.BLOCK

    if decision == "REJECT":
        return QuarantineEnrollmentDecision.REJECT

    if not decision:
        return QuarantineEnrollmentDecision.REQUEST_MORE_SHADOW_DATA

    if decision == "REQUEST_REHEARSAL_RETEST":
        return QuarantineEnrollmentDecision.REQUEST_REHEARSAL_RETEST

    if decision == "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE":
        if score is not None and score >= min_score:
            if QuarantineSafetyFlag.LOW_SHADOW_ACCEPTANCE_SCORE in safety_flags:
                return QuarantineEnrollmentDecision.REQUEST_MANUAL_REVIEW
            return QuarantineEnrollmentDecision.ENROLL_AS_QUARANTINED_CANDIDATE
        elif score is not None and score < min_score:
            return QuarantineEnrollmentDecision.REQUEST_MANUAL_REVIEW
        else:
            return QuarantineEnrollmentDecision.REQUEST_MORE_SHADOW_DATA

    return QuarantineEnrollmentDecision.REQUEST_MANUAL_REVIEW

def quarantine_eligibility_reasons(shadow_governance_payload: dict[str, Any], min_score: float = 70.0) -> list[str]:
    reasons = []
    decision = extract_shadow_governance_decision(shadow_governance_payload)
    score = extract_shadow_acceptance_score(shadow_governance_payload)

    if decision == "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE" and score is not None and score >= min_score:
        reasons.append(f"Shadow governance accepted with score {score} >= {min_score}")
    elif score is not None and score < min_score:
         reasons.append(f"Score {score} is below minimum {min_score}")
    else:
         reasons.append(f"Decision was {decision}")

    return reasons

def candidate_status_from_enrollment_decision(decision: QuarantineEnrollmentDecision) -> QuarantineCandidateStatus:
    if decision == QuarantineEnrollmentDecision.ENROLL_AS_QUARANTINED_CANDIDATE:
        return QuarantineCandidateStatus.ENROLLED
    elif decision == QuarantineEnrollmentDecision.REQUEST_MANUAL_REVIEW:
        return QuarantineCandidateStatus.WAITING_MANUAL_REVIEW
    elif decision == QuarantineEnrollmentDecision.BLOCK:
        return QuarantineCandidateStatus.BLOCKED
    elif decision == QuarantineEnrollmentDecision.REJECT:
        return QuarantineCandidateStatus.REJECTED
    else:
        return QuarantineCandidateStatus.ELIGIBLE

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_quarantine_eligibility(payload)
    status = candidate_status_from_enrollment_decision(decision)
    reasons = quarantine_eligibility_reasons(payload)

    lines = [
        f"Enrollment Decision: {decision.value}",
        f"Candidate Status: {status.value}",
        f"Reasons: {reasons}",
    ]
    return "\n".join(lines)
