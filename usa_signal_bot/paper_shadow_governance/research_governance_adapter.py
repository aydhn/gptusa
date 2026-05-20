from typing import Any, Dict
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowGovernanceReview, ShadowDecisionBoardResult

def attach_shadow_governance_to_research_governance_payload(governance_payload: Dict[str, Any], shadow_governance_review: ShadowGovernanceReview) -> Dict[str, Any]:
    res = governance_payload.copy()
    res["shadow_governance"] = shadow_governance_review.__dict__
    return res

def shadow_decision_to_research_governance_hint(result: ShadowDecisionBoardResult) -> Dict[str, Any]:
    return {"hint": "Shadow Rehearsal: " + result.decision.value}

def research_governance_shadow_summary(governance_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"has_shadow_governance": "shadow_governance" in governance_payload}

def research_governance_adapter_to_text(payload: Dict[str, Any]) -> str:
    return str(payload)
