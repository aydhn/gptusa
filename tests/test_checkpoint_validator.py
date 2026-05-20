import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.human_review_checkpoint import build_human_review_checkpoint
from usa_signal_bot.paper_dry_run_bridge.checkpoint_validator import (
    validate_checkpoint_safety,
    checkpoint_requires_followup,
    checkpoint_expired,
    checkpoint_validator_summary,
    checkpoint_validator_to_text
)

def test_checkpoint_validator():
    ctx = build_mock_dry_run_bridge_context()
    chk = build_human_review_checkpoint(ctx)

    errors = validate_checkpoint_safety(chk)
    assert len(errors) == 0

    chk_bad = build_human_review_checkpoint(ctx)
    chk_bad.allows_active_paper = True
    errors_bad = validate_checkpoint_safety(chk_bad)
    assert len(errors_bad) > 0

    assert checkpoint_requires_followup(chk) is True

    assert checkpoint_expired(chk) is False

    summary = checkpoint_validator_summary(chk)
    assert summary["safe"] is True

    assert "Validation" in checkpoint_validator_to_text(summary)
