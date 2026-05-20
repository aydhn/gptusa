from typing import Any, Dict
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowSessionComparisonReport, ShadowGovernanceReview
from usa_signal_bot.paper_shadow_governance.comparison_report import build_full_shadow_comparison_report

def shadow_comparison_from_sandbox_reviews(baseline_sandbox_payload: Dict[str, Any], candidate_sandbox_payload: Dict[str, Any]) -> ShadowSessionComparisonReport:
    bp = baseline_sandbox_payload.get("shadow_session", {})
    cp = candidate_sandbox_payload.get("shadow_session", {})
    return build_full_shadow_comparison_report(bp, cp)

def attach_shadow_governance_to_sandbox_review(sandbox_payload: Dict[str, Any], governance_review: ShadowGovernanceReview) -> Dict[str, Any]:
    res = sandbox_payload.copy()
    res["shadow_governance"] = governance_review.__dict__
    return res

def release_sandbox_shadow_governance_summary(sandbox_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"has_governance": "shadow_governance" in sandbox_payload}

def release_sandbox_adapter_to_text(payload: Dict[str, Any]) -> str:
    return str(payload)
