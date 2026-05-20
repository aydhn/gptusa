import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.proposal_generator import generate_dry_run_proposals
from usa_signal_bot.paper_dry_run_bridge.risk_evaluator import (
    evaluate_dry_run_proposals_risk,
    dry_run_risk_summary,
    dry_run_risk_evaluator_to_text
)
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunProposalStatus

def test_risk_evaluator():
    ctx = build_mock_dry_run_bridge_context()
    proposals = generate_dry_run_proposals(ctx)

    evaluated = evaluate_dry_run_proposals_risk(proposals, ctx)

    for p in evaluated:
        assert p.status in [DryRunProposalStatus.RISK_ACCEPTED, DryRunProposalStatus.RISK_WARNING, DryRunProposalStatus.RISK_REJECTED, DryRunProposalStatus.BLOCKED]

    proposals[0].is_real_order = True
    evaluated_bad = evaluate_dry_run_proposals_risk([proposals[0]], ctx)
    assert evaluated_bad[0].status == DryRunProposalStatus.BLOCKED

    summary = dry_run_risk_summary(evaluated)
    assert "accepted" in summary

    assert "Risk Evaluation" in dry_run_risk_evaluator_to_text(summary)
