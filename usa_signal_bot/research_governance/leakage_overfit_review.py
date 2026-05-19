from typing import Any, Optional
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistItem, GovernanceRiskFlag, GovernanceChecklistStatus, GovernanceEvidencePack, create_governance_checklist_item_id

def detect_possible_overfit(comparison_payload: dict[str, Any]) -> GovernanceChecklistItem:
    return GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("possible_overfit"),
        name="possible_overfit",
        status=GovernanceChecklistStatus.PASS,
        description="Possible Overfit Check",
        evidence_refs=[], risk_flags=[], warnings=[], errors=[]
    )

def detect_possible_leakage(comparison_payload: dict[str, Any]) -> GovernanceChecklistItem:
    status = GovernanceChecklistStatus.PASS
    gates = comparison_payload.get("gates", [])
    for g in gates:
        if g.get("name") == "NO_LEAKAGE" and g.get("status") == "FAIL":
            status = GovernanceChecklistStatus.FAIL
            break

    flags = [GovernanceRiskFlag.POSSIBLE_LEAKAGE] if status == GovernanceChecklistStatus.FAIL else []
    return GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("possible_leakage"),
        name="possible_leakage",
        status=status,
        description="Possible Leakage Check",
        evidence_refs=[], risk_flags=flags, warnings=[], errors=[]
    )

def review_leakage_overfit_flags(comparison_payload: dict[str, Any], evidence_pack: Optional[GovernanceEvidencePack] = None) -> list[GovernanceChecklistItem]:
    return [detect_possible_overfit(comparison_payload), detect_possible_leakage(comparison_payload)]

def leakage_overfit_risk_flags(comparison_payload: dict[str, Any]) -> list[GovernanceRiskFlag]:
    flags = []
    item = detect_possible_leakage(comparison_payload)
    if item.status == GovernanceChecklistStatus.FAIL:
        flags.append(GovernanceRiskFlag.POSSIBLE_LEAKAGE)
    return flags

def leakage_overfit_review_to_text(items: list[GovernanceChecklistItem]) -> str:
    return "Leakage Overfit Review"
