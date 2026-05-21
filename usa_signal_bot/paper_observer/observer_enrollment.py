from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PaperObserverEnrollmentStatus, ObserverSafetyFlag
from usa_signal_bot.paper_observer.observer_models import (
    PaperObserverEnrollment,
    LockedObserverPolicy,
    create_paper_observer_enrollment_id
)
from usa_signal_bot.paper_observer.locked_observer_policy import default_locked_observer_policy
from usa_signal_bot.paper_observer.controlled_planning_ingestion import (
    extract_planning_candidate_id,
    extract_approval_status,
    extract_planning_ticket_payload,
    extract_final_approval_queue_item
)
from usa_signal_bot.paper_observer.eligibility_checker import (
    evaluate_observer_enrollment_eligibility,
    observer_safety_flags_from_controlled_planning
)

def build_observer_enrollment(candidate_id: Optional[str], planning_ticket_id: Optional[str], approval_status: Optional[str]) -> PaperObserverEnrollment:
    status = PaperObserverEnrollmentStatus.ELIGIBLE if approval_status == "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE" else PaperObserverEnrollmentStatus.DRAFT

    return PaperObserverEnrollment(
        enrollment_id=create_paper_observer_enrollment_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        candidate_id=candidate_id,
        planning_ticket_id=planning_ticket_id,
        approval_queue_item_id=None,
        source_controlled_planning_review_id=None,
        source_approval_status=approval_status,
        policy=default_locked_observer_policy(),
        allowed_for_active_paper=False,
        allowed_for_broker_execution=False,
        allowed_for_paper_state_mutation=False,
        allowed_for_config_patch=False,
        safety_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_observer_enrollment_from_controlled_planning(payload: dict[str, Any]) -> PaperObserverEnrollment:
    candidate_id = extract_planning_candidate_id(payload)
    approval_status = extract_approval_status(payload)

    ticket = extract_planning_ticket_payload(payload)
    planning_ticket_id = ticket.get("ticket_id") if ticket else None

    app_queue = extract_final_approval_queue_item(payload)
    approval_queue_item_id = app_queue.get("item_id") if app_queue else None

    enrollment = build_observer_enrollment(candidate_id, planning_ticket_id, approval_status)
    enrollment.approval_queue_item_id = approval_queue_item_id
    enrollment.source_controlled_planning_review_id = payload.get("review_id")
    enrollment.status = evaluate_observer_enrollment_eligibility(payload)
    enrollment.safety_flags = observer_safety_flags_from_controlled_planning(payload)

    return enrollment

def validate_observer_enrollment_safety(enrollment: PaperObserverEnrollment) -> List[str]:
    errors = []
    if enrollment.allowed_for_active_paper:
        errors.append("Enrollment cannot be allowed for active paper")
    if enrollment.allowed_for_broker_execution:
        errors.append("Enrollment cannot be allowed for broker execution")
    if enrollment.allowed_for_paper_state_mutation:
        errors.append("Enrollment cannot be allowed for paper state mutation")
    if enrollment.allowed_for_config_patch:
        errors.append("Enrollment cannot be allowed for config patch")
    if enrollment.policy and not enrollment.policy.locked_runtime:
        errors.append("Policy must have locked_runtime=True")
    return errors

def observer_enrollment_summary(enrollment: PaperObserverEnrollment) -> dict[str, Any]:
    return {
        "enrollment_id": enrollment.enrollment_id,
        "status": enrollment.status.value,
        "candidate_id": enrollment.candidate_id,
        "safety_flags": [f.value for f in enrollment.safety_flags]
    }

def observer_enrollment_to_text(enrollment: PaperObserverEnrollment) -> str:
    return f"PaperObserverEnrollment {enrollment.enrollment_id} - {enrollment.status.value} for candidate {enrollment.candidate_id}"
