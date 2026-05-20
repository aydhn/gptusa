from typing import Any, List
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunProposal,
    DryRunProposalStatus,
    DryRunProposalType
)

def evaluate_dry_run_proposal_risk(proposal: DryRunProposal, context: DryRunBridgeContext) -> DryRunProposal:
    warnings = dry_run_risk_warnings(proposal, context)

    if proposal.is_real_order or proposal.will_mutate_paper_state or proposal.will_send_to_broker:
        proposal.status = DryRunProposalStatus.BLOCKED
        proposal.errors.append("Proposal violates fundamental safety guards (real order, paper mutation, broker send).")
    elif len(warnings) > 0:
        if any("oversize" in w.lower() for w in warnings):
            proposal.status = DryRunProposalStatus.RISK_REJECTED
        else:
            proposal.status = DryRunProposalStatus.RISK_WARNING
        proposal.warnings.extend(warnings)
    else:
        proposal.status = DryRunProposalStatus.RISK_ACCEPTED

    return proposal

def evaluate_dry_run_proposals_risk(proposals: List[DryRunProposal], context: DryRunBridgeContext) -> List[DryRunProposal]:
    return [evaluate_dry_run_proposal_risk(p, context) for p in proposals]

def dry_run_risk_warnings(proposal: DryRunProposal, context: DryRunBridgeContext) -> List[str]:
    warnings = []
    if proposal.notional_usd and proposal.notional_usd > 100000:
        warnings.append("Oversize notional amount detected.")
    if not proposal.symbol and proposal.proposal_type in [DryRunProposalType.SIGNAL_PROPOSAL, DryRunProposalType.ORDER_INTENT_PROPOSAL]:
        warnings.append("Missing symbol for trade proposal.")
    return warnings

def dry_run_risk_summary(proposals: List[DryRunProposal]) -> dict[str, Any]:
    return {
        "accepted": len([p for p in proposals if p.status == DryRunProposalStatus.RISK_ACCEPTED]),
        "warning": len([p for p in proposals if p.status == DryRunProposalStatus.RISK_WARNING]),
        "rejected": len([p for p in proposals if p.status == DryRunProposalStatus.RISK_REJECTED]),
        "blocked": len([p for p in proposals if p.status == DryRunProposalStatus.BLOCKED])
    }

def dry_run_risk_evaluator_to_text(payload: dict[str, Any]) -> str:
    return f"Risk Evaluation: {payload.get('accepted', 0)} accepted, {payload.get('blocked', 0)} blocked."
