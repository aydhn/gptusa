from typing import Any
from usa_signal_bot.paper_quarantine.quarantine_models import (
    PaperSnapshotRef,
    QuarantinedPaperCandidate,
    QuarantineEnrollmentReview,
)
from usa_signal_bot.paper_quarantine.paper_snapshot_ref import build_read_only_paper_snapshot_ref

def build_read_only_paper_snapshot_for_quarantine(paper_payload: dict[str, Any] | None = None) -> PaperSnapshotRef:
    return build_read_only_paper_snapshot_ref(paper_payload, source="paper_runtime_adapter")

def compare_quarantine_candidate_to_paper_snapshot(candidate: QuarantinedPaperCandidate, snapshot_ref: PaperSnapshotRef) -> dict[str, Any]:
    return {
        "candidate_id": candidate.candidate_id,
        "snapshot_hash": snapshot_ref.snapshot_hash,
        "match": False, # Mock
        "diff_keys": ["mock_diff"],
    }

def validate_paper_payload_not_mutated(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    errors = []
    # simplified mock check
    if before.get("timestamp") != after.get("timestamp") and "timestamp" in before:
        errors.append("Paper payload mutated (timestamp changed)")
    if after.get("paper_state_committed", False):
         errors.append("paper_state_committed is True")
    if after.get("paper_order_executed", False):
         errors.append("paper_order_executed is True")
    if after.get("portfolio_state_mutated", False):
         errors.append("portfolio_state_mutated is True")
    return errors

def attach_quarantine_metadata_to_paper_analytics(payload: dict[str, Any], review: QuarantineEnrollmentReview) -> dict[str, Any]:
    if review.candidates:
        payload["quarantine_candidate_id"] = review.candidates[0].candidate_id
    payload["paper_state_committed"] = False
    payload["paper_order_executed"] = False
    payload["portfolio_state_mutated"] = False
    return payload

def paper_runtime_quarantine_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Paper Runtime Quarantine Adapter\nCandidate: {payload.get('quarantine_candidate_id')}"
