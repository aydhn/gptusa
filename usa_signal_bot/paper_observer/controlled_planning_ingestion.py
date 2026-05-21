from typing import Any, Tuple, Optional, List
from usa_signal_bot.core.enums import ApprovalQueueItemStatus
from usa_signal_bot.core.exceptions import ObserverControlledPlanningIngestionError

def extract_planning_ticket_payload(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("planning_ticket")

def extract_final_approval_queue_item(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("final_approval")

def extract_planning_candidate_id(payload: dict[str, Any]) -> Optional[str]:
    ticket = extract_planning_ticket_payload(payload)
    if ticket:
        return ticket.get("candidate_id")
    return None

def extract_approval_status(payload: dict[str, Any]) -> Optional[str]:
    item = extract_final_approval_queue_item(payload)
    if item:
        return item.get("status")
    return None

def controlled_planning_supports_observer(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    status = extract_approval_status(payload)
    if status == ApprovalQueueItemStatus.APPROVED_FOR_NEXT_NON_EXECUTING_STAGE.value:
        return True, warnings
    warnings.append(f"Approval status is not APPROVED_FOR_NEXT_NON_EXECUTING_STAGE: {status}")
    return False, warnings

def ingest_controlled_planning_review(payload: dict[str, Any]) -> dict[str, Any]:
    if "report_type" not in payload:
        raise ObserverControlledPlanningIngestionError("Invalid payload: Missing report_type")

    return payload

def controlled_planning_ingestion_to_text(payload: dict[str, Any]) -> str:
    status = extract_approval_status(payload)
    candidate_id = extract_planning_candidate_id(payload)
    return f"Controlled Planning Ingestion: Candidate {candidate_id}, Status {status}"
