from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionDossierFullReview

def build_read_only_paper_snapshot_for_dry_admission_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = paper_payload or {}
    return {
        "paper_state_committed": False,
        "paper_order_executed": False,
        "portfolio_state_mutated": False,
        "is_read_only_snapshot": True,
        "original_payload_keys": list(payload.keys())
    }

def build_rehearsal_blocker_snapshot_for_dry_admission_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_read_only_paper_snapshot_for_dry_admission_dossier(paper_payload)

def compare_dry_admission_dossier_to_paper_snapshot(review: DryAdmissionDossierFullReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "snapshot_read_only": paper_snapshot.get("is_read_only_snapshot", False),
        "mutation_risk": not paper_snapshot.get("is_read_only_snapshot", False)
    }

def validate_paper_runtime_not_mutated_by_dry_admission_dossier(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    errors = []
    if before.get("paper_state_committed") != after.get("paper_state_committed"):
        errors.append("Paper state committed changed")
    if before.get("paper_order_executed") != after.get("paper_order_executed"):
        errors.append("Paper order executed changed")
    if before.get("portfolio_state_mutated") != after.get("portfolio_state_mutated"):
        errors.append("Portfolio state mutated changed")
    return errors

def attach_dry_admission_dossier_metadata_to_paper_analytics(payload: dict[str, Any], review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    payload["dry_admission_dossier_review_id"] = review.review_id
    return payload

def paper_runtime_dry_admission_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Paper Runtime Adapter: {payload.get('dry_admission_dossier_review_id')}"
