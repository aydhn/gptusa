import pytest
from usa_signal_bot.paper_dry_run_bridge.paper_quarantine_adapter import (
    dry_run_context_from_quarantine_review,
    dry_run_session_from_quarantine_review,
    dry_run_review_from_quarantine_review,
    attach_dry_run_metadata_to_quarantine_payload,
    paper_quarantine_dry_run_summary,
    paper_quarantine_adapter_to_text
)

def test_paper_quarantine_adapter():
    payload = {"candidate": {"candidate_id": "cand_1"}}

    ctx = dry_run_context_from_quarantine_review(payload)
    assert ctx.candidate_id == "cand_1"

    session = dry_run_session_from_quarantine_review(payload)
    assert session.context.candidate_id == "cand_1"

    review = dry_run_review_from_quarantine_review(payload)
    assert len(review.sessions) == 1

    payload_attached = attach_dry_run_metadata_to_quarantine_payload(payload, review)
    assert "dry_run_bridge_metadata" in payload_attached

    summary = paper_quarantine_dry_run_summary(payload_attached)
    assert summary["has_dry_run_metadata"] is True

    assert "Quarantine Adapter" in paper_quarantine_adapter_to_text(payload_attached)
