from typing import Any, Dict
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowSessionComparisonReport, ShadowGovernanceReview
from usa_signal_bot.paper_shadow_governance.comparison_report import build_full_shadow_comparison_report, build_shadow_governance_review

def comparison_from_shadow_sessions(baseline_session_payload: Dict[str, Any], candidate_session_payload: Dict[str, Any]) -> ShadowSessionComparisonReport:
    return build_full_shadow_comparison_report(baseline_session_payload, candidate_session_payload)

def governance_review_from_shadow_rehearsal_review(shadow_review_payload: Dict[str, Any]) -> ShadowGovernanceReview:
    bp = shadow_review_payload.get("baseline_session", {})
    cp = shadow_review_payload.get("candidate_session", {})
    return build_shadow_governance_review(bp, cp)

def attach_governance_to_shadow_rehearsal_review(shadow_review_payload: Dict[str, Any], governance_review: ShadowGovernanceReview) -> Dict[str, Any]:
    res = shadow_review_payload.copy()
    res["shadow_governance"] = governance_review.__dict__
    return res

def paper_shadow_governance_summary(shadow_review_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"has_governance": "shadow_governance" in shadow_review_payload}

def paper_shadow_adapter_to_text(payload: Dict[str, Any]) -> str:
    return str(payload)
