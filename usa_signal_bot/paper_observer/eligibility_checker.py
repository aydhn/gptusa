from typing import Any, List, Optional
from usa_signal_bot.core.enums import PaperObserverEnrollmentStatus, ApprovalQueueItemStatus, ObserverSafetyFlag
from usa_signal_bot.paper_observer.controlled_planning_ingestion import (
    extract_approval_status,
    controlled_planning_supports_observer
)

def observer_status_from_approval_status(status: Optional[str]) -> PaperObserverEnrollmentStatus:
    if status == ApprovalQueueItemStatus.APPROVED_FOR_NEXT_NON_EXECUTING_STAGE.value:
        return PaperObserverEnrollmentStatus.ELIGIBLE
    if status == ApprovalQueueItemStatus.WAITING_REVIEW.value:
        return PaperObserverEnrollmentStatus.DRAFT
    if status == ApprovalQueueItemStatus.REJECTED.value:
        return PaperObserverEnrollmentStatus.REJECTED
    if status in [ApprovalQueueItemStatus.BLOCKED.value, ApprovalQueueItemStatus.EXPIRED.value]:
        return PaperObserverEnrollmentStatus.BLOCKED

    return PaperObserverEnrollmentStatus.BLOCKED

def evaluate_observer_enrollment_eligibility(controlled_planning_payload: dict[str, Any]) -> PaperObserverEnrollmentStatus:
    status = extract_approval_status(controlled_planning_payload)
    return observer_status_from_approval_status(status)

def observer_eligibility_reasons(controlled_planning_payload: dict[str, Any]) -> List[str]:
    reasons = []
    status = extract_approval_status(controlled_planning_payload)
    if not status:
        reasons.append("Missing approval status in payload.")
    else:
        reasons.append(f"Approval status is {status}.")
    return reasons

def observer_safety_flags_from_controlled_planning(payload: dict[str, Any]) -> List[ObserverSafetyFlag]:
    flags = []
    status = extract_approval_status(payload)
    if not status:
        flags.append(ObserverSafetyFlag.MISSING_HUMAN_APPROVAL)
    if "planning_ticket" not in payload:
        flags.append(ObserverSafetyFlag.MISSING_PLANNING_TICKET)
    return flags

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    status = evaluate_observer_enrollment_eligibility(payload)
    reasons = observer_eligibility_reasons(payload)
    return f"Eligibility: {status.value} - {', '.join(reasons)}"
