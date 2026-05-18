from typing import Optional
from usa_signal_bot.research_governance.governance_models import GovernanceRiskFlag, GovernanceEvidencePack, PromotionDecision, GovernanceChecklistItem, GovernanceChecklistStatus, create_governance_checklist_item_id

def manual_review_required_for_flags(flags: list[GovernanceRiskFlag]) -> bool:
    return len(flags) > 0

def manual_review_required_for_evidence_pack(pack: GovernanceEvidencePack) -> bool:
    return pack.status.value != "COMPLETE"

def manual_review_required_for_decision(decision: PromotionDecision) -> bool:
    return True

def build_manual_review_checklist(flags: list[GovernanceRiskFlag], pack: Optional[GovernanceEvidencePack] = None) -> list[GovernanceChecklistItem]:
    status = GovernanceChecklistStatus.FAIL if manual_review_required_for_flags(flags) else GovernanceChecklistStatus.PASS
    return [GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("manual_review"),
        name="manual_review_required",
        status=status,
        description="Manual Review Flag",
        evidence_refs=[], risk_flags=[], warnings=[], errors=[]
    )]

def manual_review_to_text(items: list[GovernanceChecklistItem]) -> str:
    return "Manual Review Checklist"
