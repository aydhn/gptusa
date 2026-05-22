from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    RuntimeWriteLockProofRefresh,
    DryAdmissionFullReview
)
from usa_signal_bot.paper_dry_admission.write_lock_proof_refresh import refresh_runtime_write_lock_proof

def build_read_only_paper_snapshot_for_dry_admission(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not paper_payload:
        return {"state_hash": "empty_snapshot", "read_only": True}

    snapshot = paper_payload.copy()
    snapshot["read_only"] = True
    snapshot["paper_state_committed"] = False
    snapshot["paper_order_executed"] = False
    snapshot["portfolio_state_mutated"] = False

    # We do not write to paper_store here, just returning a dict.
    return snapshot

def build_runtime_write_lock_refresh_for_dry_admission(
    no_write_payload: dict[str, Any] | None = None,
    paper_payload: dict[str, Any] | None = None
) -> RuntimeWriteLockProofRefresh:
    snapshot = build_read_only_paper_snapshot_for_dry_admission(paper_payload)
    return refresh_runtime_write_lock_proof(no_write_payload, snapshot, snapshot)

def compare_dry_admission_to_paper_snapshot(review: DryAdmissionFullReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    run = review.runs[-1] if review.runs else None

    hash_match = False
    if run and run.read_only_snapshot_hash and paper_snapshot:
        snap_hash = paper_snapshot.get("state_hash") or paper_snapshot.get("hash")
        hash_match = (run.read_only_snapshot_hash == snap_hash)

    return {
        "has_run": run is not None,
        "hash_match": hash_match
    }

def validate_paper_runtime_not_mutated_by_dry_admission(before: dict[str, Any], after: dict[str, Any]) -> List[str]:
    issues = []

    hash_b = before.get("state_hash") or before.get("hash")
    hash_a = after.get("state_hash") or after.get("hash")

    if hash_b != hash_a:
        issues.append(f"Hash changed from {hash_b} to {hash_a}")

    if after.get("paper_state_committed", False):
        issues.append("paper_state_committed is True")

    if after.get("paper_order_executed", False):
        issues.append("paper_order_executed is True")

    if after.get("portfolio_state_mutated", False):
        issues.append("portfolio_state_mutated is True")

    return issues

def attach_dry_admission_metadata_to_paper_analytics(payload: dict[str, Any], review: DryAdmissionFullReview) -> dict[str, Any]:
    new_payload = payload.copy()
    new_payload["dry_admission_metadata"] = {
        "review_id": review.review_id,
        "run_status": review.runs[-1].status.value if review.runs else "UNKNOWN"
    }
    return new_payload

def paper_runtime_dry_admission_adapter_to_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Read Only: {payload.get('read_only', False)}",
        f"State Hash: {payload.get('state_hash', 'Unknown')}"
    ]
    return "\n".join(lines)
