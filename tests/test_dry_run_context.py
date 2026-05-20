import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import (
    build_dry_run_bridge_context,
    build_mock_dry_run_bridge_context,
    validate_dry_run_context_safety,
    dry_run_context_summary,
    dry_run_context_to_text
)

def test_dry_run_context():
    quarantine = {"candidate": {"candidate_id": "cand_1"}}
    ticket = {"ticket_id": "tick_1"}
    plan = {"bridge_plan_id": "plan_1"}
    snapshot = {"snapshot_id": "snap_1"}

    ctx = build_dry_run_bridge_context(quarantine, ticket, plan, snapshot)

    assert ctx.candidate_id == "cand_1"
    assert ctx.ticket_id == "tick_1"
    assert ctx.bridge_plan_id == "plan_1"
    assert ctx.allow_paper_state_mutation is False
    assert ctx.allow_broker_orders is False

    assert len(validate_dry_run_context_safety(ctx)) == 0

    summary = dry_run_context_summary(ctx)
    assert summary["candidate_id"] == "cand_1"

    assert "cand_1" not in dry_run_context_to_text(ctx) # Actually context_id and mode
    assert ctx.mode.value in dry_run_context_to_text(ctx)
