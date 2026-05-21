from typing import Any, Dict, List
from usa_signal_bot.core.enums import GuardedHandoffDecision, ReadinessRehearsalRiskFlag, ReadinessRehearsalStatus
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    ReadinessRehearsalRun, FinalReviewLock, HandoffEvidenceIndex
)
from usa_signal_bot.paper_readiness_rehearsal.final_lock_validator import validate_final_lock_safety

def determine_guarded_handoff_decision(run: ReadinessRehearsalRun, lock: FinalReviewLock, evidence_index: HandoffEvidenceIndex) -> GuardedHandoffDecision:
    if run.safety_flags or validate_final_lock_safety(lock):
        return GuardedHandoffDecision.BLOCK

    if run.status in [ReadinessRehearsalStatus.FAILED, ReadinessRehearsalStatus.BLOCKED]:
        return GuardedHandoffDecision.REQUEST_REHEARSAL_RERUN

    if not lock.locked or lock.status.value.startswith("LOCK_BLOCKED"):
        return GuardedHandoffDecision.REQUEST_REHEARSAL_RERUN

    if evidence_index.missing_evidence_types or evidence_index.stale_evidence_types:
        return GuardedHandoffDecision.REQUEST_DOSSIER_REFRESH

    if evidence_index.evidence_score is None or evidence_index.evidence_score < 100.0:
        return GuardedHandoffDecision.REQUEST_DOSSIER_REFRESH

    return GuardedHandoffDecision.REGISTER_FOR_FINAL_NON_EXECUTING_HANDOFF_REVIEW

def guarded_handoff_decision_reasons(decision: GuardedHandoffDecision, flags: List[ReadinessRehearsalRiskFlag]) -> List[str]:
    reasons = [f"Decision: {decision.value}"]
    if flags:
        reasons.append(f"Blocked due to safety flags: {[f.value for f in flags]}")
    return reasons

def guarded_handoff_required_followups(decision: GuardedHandoffDecision, flags: List[ReadinessRehearsalRiskFlag]) -> List[str]:
    if decision == GuardedHandoffDecision.BLOCK:
        return ["Resolve critical safety blocks immediately"]
    elif decision == GuardedHandoffDecision.REQUEST_REHEARSAL_RERUN:
        return ["Re-run stage rehearsal plans"]
    elif decision == GuardedHandoffDecision.REQUEST_DOSSIER_REFRESH:
        return ["Refresh promotion dossier evidence"]
    elif decision == GuardedHandoffDecision.REQUEST_MANUAL_REVIEW:
        return ["Perform manual review of handoff entry"]
    elif decision == GuardedHandoffDecision.REGISTER_FOR_FINAL_NON_EXECUTING_HANDOFF_REVIEW:
        return ["Proceed to final non-executing handoff review"]
    return ["Unknown followups required"]

def guarded_handoff_allows_next_review(decision: GuardedHandoffDecision) -> bool:
    return decision == GuardedHandoffDecision.REGISTER_FOR_FINAL_NON_EXECUTING_HANDOFF_REVIEW

def handoff_decision_metadata_to_text(payload: Dict[str, Any]) -> str:
    return f"Handoff Decision: {payload.get('decision', 'UNKNOWN')}"
