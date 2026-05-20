import pytest
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.paper_shadow_governance_adapter import (
    dry_run_candidate_refs_from_shadow_governance,
    shadow_governance_supports_dry_run,
    attach_dry_run_hint_to_shadow_governance,
    paper_shadow_governance_dry_run_summary,
    paper_shadow_governance_adapter_to_text
)

def test_shadow_governance_adapter():
    payload = {"candidate_id": "cand_1", "review_id": "rev_1"}

    refs = dry_run_candidate_refs_from_shadow_governance(payload)
    assert refs["candidate_id"] == "cand_1"

    supports, _ = shadow_governance_supports_dry_run(payload)
    assert supports is True

    ctx = build_mock_dry_run_bridge_context()
    runner = SupervisedDryRunBridgeRunner()
    session = runner.run_session(ctx)

    payload_attached = attach_dry_run_hint_to_shadow_governance(payload, session)
    assert "dry_run_hint" in payload_attached

    summary = paper_shadow_governance_dry_run_summary(payload_attached)
    assert summary["has_dry_run_hint"] is True

    assert "Shadow Governance Adapter" in paper_shadow_governance_adapter_to_text(payload_attached)
