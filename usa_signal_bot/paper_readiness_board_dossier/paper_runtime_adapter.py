from typing import Any
import json
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import BoardDossierFullReview

def build_read_only_paper_snapshot_for_board_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = paper_payload or {}
    # Ensures read-only flags
    snapshot = dict(payload)
    snapshot["read_only"] = True
    snapshot["write_blocked"] = True
    snapshot["paper_state_committed"] = False
    snapshot["paper_order_executed"] = False
    snapshot["portfolio_state_mutated"] = False
    snapshot["broker_order_sent"] = False
    return snapshot

def build_shadow_launch_blocker_snapshot_for_board_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = paper_payload or {}
    # Specific snapshot that implies shadow launch is blocked
    snapshot = dict(payload)
    snapshot["shadow_launch_allowed"] = False
    snapshot["paper_mode_launch_allowed"] = False
    snapshot["active_paper_enabled"] = False
    snapshot["admission_allowed"] = False
    return snapshot

def compare_board_dossier_to_paper_snapshot(review: BoardDossierFullReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    dossier = review.dossiers[0] if review.dossiers else None
    if not dossier:
        return {"matched": False, "reason": "No dossier"}

    mismatches = []

    if paper_snapshot.get("paper_state_committed") is True:
        mismatches.append("paper_state_committed=True")
    if paper_snapshot.get("paper_order_executed") is True:
        mismatches.append("paper_order_executed=True")
    if paper_snapshot.get("portfolio_state_mutated") is True:
        mismatches.append("portfolio_state_mutated=True")

    return {
        "matched": len(mismatches) == 0,
        "mismatches": mismatches
    }

def validate_paper_runtime_not_mutated_by_board_dossier(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    issues = []
    # Dump to JSON to easily detect any mutation keys changing to True
    b_json = json.dumps(before, default=str)
    a_json = json.dumps(after, default=str)

    if before != after:
        # Check specifically for dangerous mutations
        mutations = [
            "paper_state_committed",
            "paper_order_executed",
            "portfolio_state_mutated",
            "broker_order_sent"
        ]

        for m in mutations:
            b_val = before.get(m, False)
            a_val = after.get(m, False)
            if not b_val and a_val:
                issues.append(f"Dangerous mutation detected: {m} changed from False to True")

    return issues

def attach_board_dossier_metadata_to_paper_analytics(payload: dict[str, Any], review: BoardDossierFullReview) -> dict[str, Any]:
    new_payload = dict(payload)
    new_payload["board_dossier_metadata"] = {
        "review_id": review.review_id,
        "is_safe": not review.errors,
        "is_execution_blocked": True
    }
    return new_payload

def paper_runtime_board_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    metadata = payload.get("board_dossier_metadata", {})
    if not metadata:
        return "No Board Dossier metadata in Paper Analytics."
    lines = ["Paper Runtime Adapter Metadata:"]
    for k, v in metadata.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)
