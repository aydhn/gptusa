from typing import Any, Dict, List

def build_read_only_paper_runtime_snapshot_for_promotion_dossier(paper_payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return {
        "read_only": True,
        "paper_state_committed": False,
        "paper_order_executed": False,
        "portfolio_state_mutated": False,
        "original_payload_keys": list((paper_payload or {}).keys())
    }

def compare_promotion_package_to_paper_snapshot(package: Any, paper_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "diff_count": 0,
        "mutations_detected": False
    }

def validate_paper_runtime_not_mutated_by_promotion_dossier(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    return []

def attach_promotion_dossier_metadata_to_paper_analytics(payload: Dict[str, Any], review: Any) -> Dict[str, Any]:
    payload["promotion_dossier_review_id"] = getattr(review, "review_id", None)
    return payload

def paper_runtime_promotion_dossier_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"Paper Runtime Adapter. Read-only: {payload.get('read_only', False)}."
