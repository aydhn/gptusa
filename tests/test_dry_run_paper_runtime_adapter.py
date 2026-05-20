import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.paper_runtime_adapter import (
    build_read_only_paper_runtime_snapshot_for_dry_run,
    compare_dry_run_proposals_to_paper_snapshot,
    validate_paper_runtime_snapshot_not_mutated,
    attach_dry_run_metadata_to_paper_analytics,
    paper_runtime_dry_run_adapter_to_text
)

def test_paper_runtime_adapter():
    paper = {"paper_state_committed": True, "orders": [{"id": 1}]}

    snap = build_read_only_paper_runtime_snapshot_for_dry_run(paper)
    assert snap["paper_state_committed"] is False

    ctx = build_mock_dry_run_bridge_context()
    runner = SupervisedDryRunBridgeRunner()
    session = runner.run_session(ctx)

    comp = compare_dry_run_proposals_to_paper_snapshot(session.proposals, snap)
    assert comp["proposal_count"] == len(session.proposals)

    errors = validate_paper_runtime_snapshot_not_mutated(snap, snap)
    assert len(errors) == 0

    snap_mutated = snap.copy()
    snap_mutated["paper_state_committed"] = True
    errors_mutated = validate_paper_runtime_snapshot_not_mutated(snap, snap_mutated)
    assert len(errors_mutated) > 0

    analytics = attach_dry_run_metadata_to_paper_analytics({}, session)
    assert "dry_run_metadata" in analytics

    assert "Paper Runtime Adapter" in paper_runtime_dry_run_adapter_to_text(analytics)
