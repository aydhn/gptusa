from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningTicket, PaperAdjacentRehearsalContext, PaperAdjacentProposal,
    PaperAdjacentRehearsalRun, FinalHumanApprovalQueueItem, ControlledPlanningAuditEntry,
    ControlledPlanningReview, validate_controlled_planning_ticket,
    validate_paper_adjacent_rehearsal_context, validate_paper_adjacent_proposal,
    validate_final_human_approval_queue_item
)
from usa_signal_bot.core.enums import ControlledPlanningTicketStatus, PaperAdjacentRehearsalMode, ApprovalQueueItemStatus, ApprovalQueueDecision, ControlledPlanningReportType
from usa_signal_bot.core.exceptions import ControlledPlanningValidationError
import pytest

def test_models_creation():
    t = ControlledPlanningTicket("t1", "now", ControlledPlanningTicketStatus.DRAFT, "c1", None, None, None, None, [], [], [], True, True, False, False, False, False, [], [], {})
    assert t.ticket_id == "t1"

def test_validations_raise():
    t = ControlledPlanningTicket("t1", "now", ControlledPlanningTicketStatus.DRAFT, "c1", None, None, None, None, [], [], [], True, True, True, False, False, False, [], [], {})
    with pytest.raises(ControlledPlanningValidationError):
        validate_controlled_planning_ticket(t)

    c = PaperAdjacentRehearsalContext("c1", "now", "cand1", "t1", PaperAdjacentRehearsalMode.FULL_GUARDED_REHEARSAL, {}, {}, None, True, False, False, False, False, False, [], [], {})
    with pytest.raises(ControlledPlanningValidationError):
        validate_paper_adjacent_rehearsal_context(c)

    p = PaperAdjacentProposal("p1", "now", "c1", "SPY", "SIGNAL", "BUY", 10, 1000, "OK", "reason", True, False, False, [], [], {})
    with pytest.raises(ControlledPlanningValidationError):
        validate_paper_adjacent_proposal(p)

    q = FinalHumanApprovalQueueItem("q1", "now", ApprovalQueueItemStatus.QUEUED, "c1", "t1", "r1", ApprovalQueueDecision.INCONCLUSIVE, None, None, None, [], [], True, False, False, False, [], [], {})
    with pytest.raises(ControlledPlanningValidationError):
        validate_final_human_approval_queue_item(q)
