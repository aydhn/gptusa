from typing import Any
import json
from copy import deepcopy
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import NoOrderDossierFullReview

def build_read_only_paper_snapshot_for_no_order_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not paper_payload:
        return {
            "is_read_only": True,
            "paper_state_committed": False,
            "paper_order_executed": False,
            "portfolio_state_mutated": False
        }
    snapshot = deepcopy(paper_payload)
    snapshot["is_read_only"] = True
    snapshot["paper_state_committed"] = False
    snapshot["paper_order_executed"] = False
    snapshot["portfolio_state_mutated"] = False
    return snapshot

def build_admission_blocker_snapshot_for_no_order_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    snapshot = build_read_only_paper_snapshot_for_no_order_dossier(paper_payload)
    snapshot["admission_blocked"] = True
    return snapshot

def compare_no_order_dossier_to_paper_snapshot(review: NoOrderDossierFullReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "is_read_only": paper_snapshot.get("is_read_only", False),
        "safe": paper_snapshot.get("is_read_only", False) and not paper_snapshot.get("paper_state_committed", True)
    }

def validate_paper_runtime_not_mutated_by_no_order_dossier(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    reasons = []
    # Simplified check: just verify that after state matches before state for key mutation indicators
    if after.get("paper_state_committed") and not before.get("paper_state_committed"):
        reasons.append("paper_state_committed became True")
    if after.get("paper_order_executed") and not before.get("paper_order_executed"):
        reasons.append("paper_order_executed became True")
    if after.get("portfolio_state_mutated") and not before.get("portfolio_state_mutated"):
        reasons.append("portfolio_state_mutated became True")
    return reasons

def attach_no_order_dossier_metadata_to_paper_analytics(payload: dict[str, Any], review: NoOrderDossierFullReview) -> dict[str, Any]:
    out = payload.copy()
    out["no_order_dossier_review_id"] = review.review_id
    dossier = review.dossiers[0] if review.dossiers else None
    if dossier:
        out["no_order_dossier_status"] = dossier.status.value
    return out

def paper_runtime_no_order_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
