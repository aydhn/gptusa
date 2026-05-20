from typing import Any, Dict
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowGovernanceReview
from usa_signal_bot.paper_shadow_governance.comparison_report import build_shadow_governance_review

def shadow_governance_from_bundle_payloads(baseline_bundle_payload: Dict[str, Any], candidate_bundle_payload: Dict[str, Any]) -> ShadowGovernanceReview:
    bp = baseline_bundle_payload.get("shadow_session", {})
    cp = candidate_bundle_payload.get("shadow_session", {})
    return build_shadow_governance_review(bp, cp)

def attach_shadow_governance_to_bundle_payload(bundle_payload: Dict[str, Any], governance_review: ShadowGovernanceReview) -> Dict[str, Any]:
    res = bundle_payload.copy()
    res["shadow_governance"] = governance_review.__dict__
    return res

def release_packaging_shadow_governance_summary(bundle_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"has_governance": "shadow_governance" in bundle_payload}

def release_packaging_adapter_to_text(payload: Dict[str, Any]) -> str:
    return str(payload)
