from typing import Any, Dict, List, Optional
import copy
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PaperSafeDossierFullReview

def build_read_only_paper_snapshot_for_paper_safe_dossier(paper_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not paper_payload:
        return {}
    snapshot = copy.deepcopy(paper_payload)
    snapshot["is_read_only_snapshot"] = True
    snapshot["paper_state_committed"] = False
    snapshot["paper_order_executed"] = False
    snapshot["portfolio_state_mutated"] = False
    snapshot["position_mutated"] = False
    snapshot["cash_mutated"] = False
    snapshot["equity_mutated"] = False
    return snapshot

def build_pre_paper_runtime_snapshot_for_dossier(paper_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    snapshot = build_read_only_paper_snapshot_for_paper_safe_dossier(paper_payload)
    snapshot["is_pre_paper_runtime_snapshot"] = True
    return snapshot

def compare_paper_safe_dossier_to_paper_snapshot(review: PaperSafeDossierFullReview, paper_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "dossier_id": review.dossiers[0].dossier_id if review.dossiers else None,
        "is_read_only": paper_snapshot.get("is_read_only_snapshot", False),
        "mutations": paper_snapshot.get("paper_state_committed", False)
    }

def validate_paper_runtime_not_mutated_by_paper_safe_dossier(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    errors = []
    if before != after:
        errors.append("Paper runtime state was mutated by dossier.")
    return errors

def attach_paper_safe_dossier_metadata_to_paper_analytics(payload: Dict[str, Any], review: PaperSafeDossierFullReview) -> Dict[str, Any]:
    payload["paper_safe_dossier_id"] = review.dossiers[0].dossier_id if review.dossiers else None
    return payload

def paper_runtime_paper_safe_dossier_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"Paper Adapter Metadata: {payload.get('paper_safe_dossier_id')}"
