from typing import Any
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistItem, GovernanceRiskFlag, GovernanceReview

def attribution_governance_checklist(attribution_payload: dict[str, Any]) -> list[GovernanceChecklistItem]:
    return []

def attribution_governance_risk_flags(attribution_payload: dict[str, Any]) -> list[GovernanceRiskFlag]:
    return []

def attribution_governance_summary(attribution_payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def attach_governance_to_attribution_review(attribution_payload: dict[str, Any], governance_review: GovernanceReview) -> dict[str, Any]:
    attribution_payload["governance"] = governance_review.governance_review_id
    return attribution_payload

def attribution_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Attribution Adapter"
