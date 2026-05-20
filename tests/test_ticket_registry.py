import pytest
from usa_signal_bot.paper_quarantine.quarantine_models import ReadOnlyPromotionTicket
from usa_signal_bot.paper_quarantine.ticket_registry import (
    register_promotion_ticket,
    find_ticket_by_id,
    find_tickets_by_candidate_id,
    latest_ticket_for_candidate,
)

def test_registry(mocker):
    t = mocker.Mock(spec=ReadOnlyPromotionTicket)
    t.ticket_id = "t1"
    t.candidate_id = "c1"
    t.created_at_utc = "2024-01-01T00:00:00Z"

    reg = register_promotion_ticket(t)
    assert len(reg) == 1
    assert find_ticket_by_id(reg, "t1").ticket_id == t.ticket_id
    assert len(find_tickets_by_candidate_id(reg, "c1")) == 1
    assert latest_ticket_for_candidate(reg, "c1").ticket_id == t.ticket_id
