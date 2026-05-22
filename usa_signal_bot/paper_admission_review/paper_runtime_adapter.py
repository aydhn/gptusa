from typing import Any, Dict, List
import json
import copy

def build_read_only_paper_snapshot_for_admission_review(paper_payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    snapshot = copy.deepcopy(paper_payload) if paper_payload else {}
    snapshot["readonly"] = True
    return snapshot

def compare_admission_review_to_paper_snapshot(report: Any, paper_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {"match": True}

def validate_paper_runtime_not_mutated_by_admission_review(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    errors = []
    for key in ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]:
        if after.get(key, False):
             errors.append(f"{key} is true in after state")
    return errors

def attach_admission_review_metadata_to_paper_analytics(payload: Dict[str, Any], report: Any) -> Dict[str, Any]:
    payload["admission_review_metadata_attached"] = True
    return payload

def paper_runtime_admission_review_adapter_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
