import pytest
from pathlib import Path
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunBridgeReview, DryRunBridgeReportType, create_dry_run_bridge_review_id
from usa_signal_bot.paper_dry_run_bridge.dry_run_store import (
    dry_run_bridge_store_dir,
    dry_run_contexts_dir,
    write_dry_run_context_json,
    write_dry_run_session_json,
    write_dry_run_bridge_review_json,
    read_dry_run_bridge_review_json,
    dry_run_bridge_store_summary
)
from datetime import datetime, timezone

def test_dry_run_store(tmp_path: Path):
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

    data_root = tmp_path / "data"

    ctx_path = dry_run_contexts_dir(data_root) / f"{ctx.context_id}.json"
    write_dry_run_context_json(ctx_path, ctx)
    assert ctx_path.exists()

    review_path = dry_run_bridge_store_dir(data_root) / "reviews" / f"{review.review_id}.json"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    write_dry_run_bridge_review_json(review_path, review)
    assert review_path.exists()

    loaded_review = read_dry_run_bridge_review_json(review_path)
    assert loaded_review["review_id"] == review.review_id

    summary = dry_run_bridge_store_summary(data_root)
    assert summary["contexts"] == 1
    assert summary["reviews"] == 1
