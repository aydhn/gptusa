import pytest
from usa_signal_bot.paper_dry_run_bridge.ticket_ingestion import (
    ingest_promotion_ticket_payload,
    extract_ticket_id,
    extract_ticket_status,
    ticket_supports_dry_run_bridge,
    ticket_read_only_check,
    ticket_ingestion_to_text
)
from usa_signal_bot.core.enums import PromotionTicketStatus

def test_ticket_ingestion():
    payload = {
        "ticket_id": "ticket_123",
        "status": PromotionTicketStatus.APPROVED_FOR_SUPERVISED_DRY_RUN_PLANNING.value,
        "read_only": True,
        "allowed_for_active_paper": False,
        "allowed_for_config_patch": False,
        "allowed_for_broker_execution": False
    }

    assert extract_ticket_id(payload) == "ticket_123"
    assert extract_ticket_status(payload) == PromotionTicketStatus.APPROVED_FOR_SUPERVISED_DRY_RUN_PLANNING.value

    supports, _ = ticket_supports_dry_run_bridge(payload)
    assert supports is True

    assert len(ticket_read_only_check(payload)) == 0

    payload_invalid = payload.copy()
    payload_invalid["allowed_for_active_paper"] = True
    assert len(ticket_read_only_check(payload_invalid)) > 0

    assert "ticket_123" in ticket_ingestion_to_text(payload)
