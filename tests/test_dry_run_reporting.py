import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunBridgeReview, DryRunBridgeReportType, create_dry_run_bridge_review_id
from usa_signal_bot.paper_dry_run_bridge.dry_run_reporting import (
    dry_run_bridge_limitations_text,
    dry_run_context_to_text,
    dry_run_bridge_session_to_text,
    dry_run_bridge_review_to_text
)
from datetime import datetime, timezone

def test_dry_run_reporting():
    ctx = build_mock_dry_run_bridge_context()
    runner = SupervisedDryRunBridgeRunner()
    session = runner.run_session(ctx)
    review = DryRunBridgeReview(
        review_id=create_dry_run_bridge_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=DryRunBridgeReportType.FULL_DRY_RUN_BRIDGE_REVIEW,
        sessions=[session],
        telemetry_events=session.telemetry_events,
        checkpoints=session.human_checkpoints,
        output_paths={},
        warnings=[],
        errors=[]
    )

    assert "NOT active paper trading" in dry_run_bridge_limitations_text()
    assert ctx.context_id in dry_run_context_to_text(ctx)
    assert session.session_id in dry_run_bridge_session_to_text(session)
    assert review.review_id in dry_run_bridge_review_to_text(review)
