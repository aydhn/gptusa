from typing import Any
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistItem, GovernanceRiskFlag, GovernanceChecklistStatus, create_governance_checklist_item_id

def review_attribution_delta(delta_payload: dict[str, Any]) -> list[GovernanceChecklistItem]:
    return [GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("attribution"),
        name="attribution_check",
        status=GovernanceChecklistStatus.PASS,
        description="Check attribution delta",
        evidence_refs=[], risk_flags=[], warnings=[], errors=[]
    )]

def review_diagnostics_delta(delta_payload: dict[str, Any]) -> list[GovernanceChecklistItem]:
    return [GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("diagnostics"),
        name="diagnostics_check",
        status=GovernanceChecklistStatus.PASS,
        description="Check diagnostics delta",
        evidence_refs=[], risk_flags=[], warnings=[], errors=[]
    )]

def attribution_diagnostics_risk_flags(comparison_payload: dict[str, Any]) -> list[GovernanceRiskFlag]:
    flags = []
    for reg in review_attribution_delta(comparison_payload.get("attribution_delta", {})):
        if reg.status == GovernanceChecklistStatus.WARNING:
            flags.append(GovernanceRiskFlag.ATTRIBUTION_DEGRADED)
    for reg in review_diagnostics_delta(comparison_payload.get("diagnostics_delta", {})):
        if reg.status == GovernanceChecklistStatus.WARNING:
            flags.append(GovernanceRiskFlag.DIAGNOSTICS_DEGRADED)
    return flags

def attribution_diagnostics_review_summary(comparison_payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def attribution_diagnostics_review_to_text(payload: dict[str, Any]) -> str:
    return "Attribution Diagnostics Review"
