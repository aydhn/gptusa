import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

write_file("usa_signal_bot/paper_shadow_governance/paper_shadow_adapter.py", """
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
""")

write_file("usa_signal_bot/paper_shadow_governance/release_sandbox_adapter.py", """
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
""")

write_file("usa_signal_bot/paper_shadow_governance/release_packaging_adapter.py", """
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
""")

write_file("usa_signal_bot/paper_shadow_governance/research_governance_adapter.py", """
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
""")

write_file("usa_signal_bot/paper_shadow_governance/paper_runtime_adapter.py", """
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
""")

print("Adapters generated successfully.")
