import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.human_review_checkpoint import (
    build_human_review_checkpoint,
    update_human_review_checkpoint_notes,
    mark_checkpoint_observation_only,
    reject_human_review_checkpoint,
    human_review_checkpoint_summary,
    human_review_checkpoint_to_text
)
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import HumanReviewCheckpointStatus

def test_human_review_checkpoint():
    ctx = build_mock_dry_run_bridge_context()
    chk = build_human_review_checkpoint(ctx)

    assert chk.status == HumanReviewCheckpointStatus.REQUIRED
    assert chk.allows_active_paper is False

    chk = update_human_review_checkpoint_notes(chk, "Looks good", "reviewer_1")
    assert chk.status == HumanReviewCheckpointStatus.REVIEWED_WITH_NOTES

    chk = mark_checkpoint_observation_only(chk)
    assert chk.status == HumanReviewCheckpointStatus.ACCEPTED_FOR_OBSERVATION_ONLY
    assert chk.allows_active_paper is False

    chk = reject_human_review_checkpoint(chk, "Too risky")
    assert chk.status == HumanReviewCheckpointStatus.REJECTED

    summary = human_review_checkpoint_summary(chk)
    assert summary["status"] == HumanReviewCheckpointStatus.REJECTED.value

    assert chk.checkpoint_id in human_review_checkpoint_to_text(chk)
