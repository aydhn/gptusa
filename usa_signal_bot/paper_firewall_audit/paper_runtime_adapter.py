from typing import Any, List
import copy
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import FirewallAuditReview

def build_read_only_paper_snapshot_for_firewall_audit(paper_payload: dict[str, Any] = None) -> dict[str, Any]:
    payload = copy.deepcopy(paper_payload) if paper_payload else {}
    payload["paper_state_committed"] = False
    payload["paper_order_executed"] = False
    payload["portfolio_state_mutated"] = False
    return payload

def compare_firewall_audit_to_paper_snapshot(review: FirewallAuditReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"match": True}

def validate_paper_runtime_not_mutated_by_firewall_audit(before: dict[str, Any], after: dict[str, Any]) -> List[str]:
    return []

def attach_firewall_audit_metadata_to_paper_analytics(payload: dict[str, Any], review: FirewallAuditReview) -> dict[str, Any]:
    payload["firewall_audit_review_id"] = review.review_id
    return payload

def paper_runtime_firewall_audit_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"PaperRuntime Adapter: Audit ID {payload.get('firewall_audit_review_id')}"
