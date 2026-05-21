from typing import Any, List
from usa_signal_bot.paper_controlled_planning.planning_models import (
    PaperAdjacentProposal,
    PaperAdjacentRehearsalContext,
    create_paper_adjacent_proposal_id,
    _now_str
)

def build_adjacent_proposals(context: PaperAdjacentRehearsalContext) -> List[PaperAdjacentProposal]:
    # Returns a mix of signal and portfolio proposals for testing
    proposals = build_mock_adjacent_signal_proposals(context)
    proposals.extend(build_mock_adjacent_portfolio_proposals(context))
    return proposals

def build_mock_adjacent_signal_proposals(context: PaperAdjacentRehearsalContext) -> List[PaperAdjacentProposal]:
    return [
        PaperAdjacentProposal(
            proposal_id=create_paper_adjacent_proposal_id("signal"),
            created_at_utc=_now_str(),
            candidate_id=context.candidate_id,
            symbol="SPY",
            proposal_type="SIGNAL",
            side="BUY",
            quantity=10.0,
            notional_usd=5000.0,
            risk_status="APPROVED",
            reason="Deterministic Mock Signal",
            is_real_order=False,
            will_mutate_paper_state=False,
            will_send_to_broker=False,
            warnings=[],
            errors=[]
        )
    ]

def build_mock_adjacent_portfolio_proposals(context: PaperAdjacentRehearsalContext) -> List[PaperAdjacentProposal]:
    return [
        PaperAdjacentProposal(
            proposal_id=create_paper_adjacent_proposal_id("portfolio"),
            created_at_utc=_now_str(),
            candidate_id=context.candidate_id,
            symbol="QQQ",
            proposal_type="PORTFOLIO_REBALANCE",
            side="SELL",
            quantity=5.0,
            notional_usd=2000.0,
            risk_status="APPROVED",
            reason="Deterministic Mock Portfolio Adjust",
            is_real_order=False,
            will_mutate_paper_state=False,
            will_send_to_broker=False,
            warnings=[],
            errors=[]
        )
    ]

def validate_adjacent_proposals_safe(proposals: List[PaperAdjacentProposal]) -> List[str]:
    errors = []
    for p in proposals:
        if p.is_real_order:
            errors.append(f"Proposal {p.proposal_id} is_real_order is True")
        if p.will_mutate_paper_state:
            errors.append(f"Proposal {p.proposal_id} will_mutate_paper_state is True")
        if p.will_send_to_broker:
            errors.append(f"Proposal {p.proposal_id} will_send_to_broker is True")
    return errors

def adjacent_proposal_summary(proposals: List[PaperAdjacentProposal]) -> dict[str, Any]:
    return {
        "proposal_count": len(proposals),
        "types": list(set(p.proposal_type for p in proposals)),
        "is_safe": len(validate_adjacent_proposals_safe(proposals)) == 0
    }

def adjacent_proposals_to_text(proposals: List[PaperAdjacentProposal], limit: int = 50) -> str:
    lines = [
        "📝 ADJACENT PROPOSALS",
        f"Count: {len(proposals)}"
    ]
    errs = validate_adjacent_proposals_safe(proposals)
    if errs:
        lines.append("SAFETY ERRORS:")
        for e in errs:
            lines.append(f" - {e}")
    for p in proposals[:limit]:
        lines.append(f" - [{p.proposal_type}] {p.side} {p.symbol} (ID: {p.proposal_id})")
    lines.append("LIMITATION: Proposals are NOT real orders and will NOT mutate paper state.")
    return "\n".join(lines)
