import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.proposal_generator import (
    generate_dry_run_proposals,
    validate_dry_run_proposals_safe,
    dry_run_proposal_summary,
    dry_run_proposals_to_text
)

def test_proposal_generator():
    ctx = build_mock_dry_run_bridge_context()
    proposals = generate_dry_run_proposals(ctx)

    assert len(proposals) > 0

    errors = validate_dry_run_proposals_safe(proposals)
    assert len(errors) == 0

    for p in proposals:
        assert p.is_real_order is False
        assert p.will_mutate_paper_state is False
        assert p.will_send_to_broker is False

    summary = dry_run_proposal_summary(proposals)
    assert summary["total_proposals"] == len(proposals)

    assert str(len(proposals)) in dry_run_proposals_to_text(proposals)
