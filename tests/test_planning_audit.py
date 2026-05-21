from usa_signal_bot.paper_controlled_planning.planning_audit import audit_entry_from_planning_ticket, audit_entry_from_approval_queue_item
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket
from usa_signal_bot.paper_controlled_planning.approval_queue import build_final_approval_queue_item

def test_audit():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    au_t = audit_entry_from_planning_ticket(t)
    assert au_t.entity_type == "CONTROLLED_PLANNING_TICKET"

    q = build_final_approval_queue_item(t)
    au_q = audit_entry_from_approval_queue_item(q)
    assert au_q.entity_type == "FINAL_HUMAN_APPROVAL_QUEUE_ITEM"
