from typing import Any, List
from datetime import datetime, timezone
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunProposal,
    DryRunProposalType,
    DryRunProposalStatus,
    create_dry_run_proposal_id
)

def generate_dry_run_proposals(context: DryRunBridgeContext) -> List[DryRunProposal]:
    proposals = []
    proposals.extend(generate_mock_signal_proposals(context))
    proposals.extend(generate_mock_order_intent_proposals(context))
    proposals.extend(generate_mock_portfolio_proposals(context))
    return proposals

def generate_mock_signal_proposals(context: DryRunBridgeContext) -> List[DryRunProposal]:
    return [
        DryRunProposal(
            proposal_id=create_dry_run_proposal_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            proposal_type=DryRunProposalType.SIGNAL_PROPOSAL,
            status=DryRunProposalStatus.CREATED,
            symbol="SPY",
            strategy_name=context.candidate_id or "mock_strategy",
            side="BUY",
            quantity=None,
            notional_usd=None,
            price=None,
            reason="Mock signal generation",
            is_real_order=False,
            will_mutate_paper_state=False,
            will_send_to_broker=False,
            warnings=[],
            errors=[]
        )
    ]

def generate_mock_order_intent_proposals(context: DryRunBridgeContext) -> List[DryRunProposal]:
    return [
        DryRunProposal(
            proposal_id=create_dry_run_proposal_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            proposal_type=DryRunProposalType.ORDER_INTENT_PROPOSAL,
            status=DryRunProposalStatus.CREATED,
            symbol="SPY",
            strategy_name=context.candidate_id or "mock_strategy",
            side="BUY",
            quantity=10.0,
            notional_usd=1000.0,
            price=100.0,
            reason="Mock order intent",
            is_real_order=False,
            will_mutate_paper_state=False,
            will_send_to_broker=False,
            warnings=[],
            errors=[]
        )
    ]

def generate_mock_portfolio_proposals(context: DryRunBridgeContext) -> List[DryRunProposal]:
    return [
        DryRunProposal(
            proposal_id=create_dry_run_proposal_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            proposal_type=DryRunProposalType.PORTFOLIO_PROPOSAL,
            status=DryRunProposalStatus.CREATED,
            symbol=None,
            strategy_name=None,
            side=None,
            quantity=None,
            notional_usd=None,
            price=None,
            reason="Mock portfolio adjustment",
            is_real_order=False,
            will_mutate_paper_state=False,
            will_send_to_broker=False,
            warnings=[],
            errors=[]
        )
    ]

def validate_dry_run_proposals_safe(proposals: List[DryRunProposal]) -> List[str]:
    errors = []
    for p in proposals:
        if p.is_real_order:
            errors.append(f"Proposal {p.proposal_id} is marked as real order.")
        if p.will_mutate_paper_state:
            errors.append(f"Proposal {p.proposal_id} will mutate paper state.")
        if p.will_send_to_broker:
            errors.append(f"Proposal {p.proposal_id} will send to broker.")
    return errors

def dry_run_proposal_summary(proposals: List[DryRunProposal]) -> dict[str, Any]:
    return {
        "total_proposals": len(proposals),
        "types": {t.value: len([p for p in proposals if p.proposal_type == t]) for t in DryRunProposalType},
        "statuses": {s.value: len([p for p in proposals if p.status == s]) for s in DryRunProposalStatus}
    }

def dry_run_proposals_to_text(proposals: List[DryRunProposal], limit: int = 50) -> str:
    summary = dry_run_proposal_summary(proposals)
    return f"Generated {summary['total_proposals']} safe proposals."
