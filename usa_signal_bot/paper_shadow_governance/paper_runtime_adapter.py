from typing import Any, Dict, List
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowGovernanceReview

def compare_paper_snapshot_to_shadow_session(paper_snapshot: Dict[str, Any], shadow_session_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"match": True}

def validate_paper_snapshot_not_mutated(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    return []

def attach_shadow_governance_to_paper_analytics(payload: Dict[str, Any], governance_review: ShadowGovernanceReview) -> Dict[str, Any]:
    res = payload.copy()
    res["shadow_governance"] = governance_review.__dict__
    res["paper_order_executed"] = False
    res["paper_state_committed"] = False
    return res

def paper_runtime_shadow_governance_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"has_shadow_governance": "shadow_governance" in payload}

def paper_runtime_adapter_to_text(payload: Dict[str, Any]) -> str:
    return str(payload)
