from typing import Any, Tuple, List, Optional
from usa_signal_bot.core.enums import PromotionTicketStatus

def ingest_promotion_ticket_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.copy()

def extract_ticket_id(payload: dict[str, Any]) -> Optional[str]:
    return payload.get("ticket_id")

def extract_ticket_status(payload: dict[str, Any]) -> Optional[str]:
    return payload.get("status")

def ticket_supports_dry_run_bridge(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    status = extract_ticket_status(payload)
    if not status:
        return False, ["Missing ticket status"]

    warnings = []
    if status == PromotionTicketStatus.APPROVED_FOR_SUPERVISED_DRY_RUN_PLANNING.value:
        pass
    elif status in [
        PromotionTicketStatus.BLOCKED.value,
        PromotionTicketStatus.REJECTED.value,
        PromotionTicketStatus.EXPIRED.value
    ]:
        return False, [f"Ticket status {status} is not supported for dry run"]
    else:
        warnings.append(f"Ticket status {status} is not optimal for dry run")

    return True, warnings

def ticket_read_only_check(payload: dict[str, Any]) -> List[str]:
    errors = []
    if payload.get("allowed_for_active_paper", False):
        errors.append("Ticket allows active paper. This is strictly forbidden.")
    if payload.get("allowed_for_config_patch", False):
        errors.append("Ticket allows config patch. This is strictly forbidden.")
    if payload.get("allowed_for_broker_execution", False):
        errors.append("Ticket allows broker execution. This is strictly forbidden.")
    if not payload.get("read_only", True):
        errors.append("Ticket is not read-only. This is strictly forbidden.")
    return errors

def ticket_ingestion_to_text(payload: dict[str, Any]) -> str:
    ticket_id = extract_ticket_id(payload)
    status = extract_ticket_status(payload)
    return f"Ticket Ingestion: Ticket {ticket_id} (Status: {status})"
