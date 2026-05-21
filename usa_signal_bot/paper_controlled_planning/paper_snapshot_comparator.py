import copy
from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import ControlledPlanningTicket

def build_read_only_paper_snapshot_for_planning(paper_payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    if not paper_payload:
        return {"read_only": True, "state": "mock", "paper_state_committed": False, "portfolio_state_mutated": False}
    snapshot = copy.deepcopy(paper_payload)
    snapshot["read_only"] = True
    snapshot["paper_state_committed"] = False
    snapshot["paper_order_executed"] = False
    snapshot["portfolio_state_mutated"] = False
    return snapshot

def compare_candidate_to_read_only_paper_snapshot(ticket: ControlledPlanningTicket, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": ticket.candidate_id,
        "is_read_only": paper_snapshot.get("read_only", False),
        "comparison": "Mock comparison result"
    }

def validate_paper_snapshot_not_mutated(before: dict[str, Any], after: dict[str, Any]) -> List[str]:
    errors = []
    if after.get("paper_state_committed", False):
        errors.append("paper_state_committed is True in after snapshot")
    if after.get("paper_order_executed", False):
        errors.append("paper_order_executed is True in after snapshot")
    if after.get("portfolio_state_mutated", False):
        errors.append("portfolio_state_mutated is True in after snapshot")
    return errors

def paper_snapshot_comparator_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "read_only": payload.get("read_only", False),
        "paper_state_committed": payload.get("paper_state_committed", False)
    }

def paper_snapshot_comparator_to_text(payload: dict[str, Any]) -> str:
    lines = [
        "📸 READ-ONLY PAPER SNAPSHOT COMPARATOR",
        f"Read Only: {payload.get('read_only', False)}",
        f"Paper State Committed: {payload.get('paper_state_committed', False)}",
        f"Portfolio State Mutated: {payload.get('portfolio_state_mutated', False)}",
        "LIMITATION: This snapshot is copy-only and never writes to paper store."
    ]
    return "\n".join(lines)
