import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.proposal_generator import generate_dry_run_proposals
from usa_signal_bot.paper_dry_run_bridge.notification_preview import (
    build_dry_run_notification_preview,
    validate_dry_run_notification_preview_safe,
    dry_run_notification_summary,
    dry_run_notification_preview_to_text
)

def test_notification_preview():
    ctx = build_mock_dry_run_bridge_context()
    proposals = generate_dry_run_proposals(ctx)

    preview = build_dry_run_notification_preview(ctx, proposals)
    assert preview["is_real_send"] is False
    assert preview["preview_only"] is True

    errors = validate_dry_run_notification_preview_safe(preview)
    assert len(errors) == 0

    preview_bad = preview.copy()
    preview_bad["message"] = "Bu bir real order. Kesin al."
    errors_bad = validate_dry_run_notification_preview_safe(preview_bad)
    assert len(errors_bad) > 0

    summary = dry_run_notification_summary(preview)
    assert summary["is_real_send"] is False

    assert ctx.context_id in dry_run_notification_preview_to_text(preview)
