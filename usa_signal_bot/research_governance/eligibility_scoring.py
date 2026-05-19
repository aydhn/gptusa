from typing import Any, Optional
from usa_signal_bot.research_governance.governance_models import GovernanceEvidencePack, GovernanceChecklistItem, PromotionEligibility, PromotionDecision, GovernanceRiskFlag, EvidencePackStatus

def calculate_promotion_eligibility_score(evidence_pack: GovernanceEvidencePack, checklist_items: list[GovernanceChecklistItem]) -> Optional[float]:
    if evidence_pack.status == EvidencePackStatus.MISSING_REQUIRED_EVIDENCE:
        return None
    score = 100.0
    for item in checklist_items:
        if item.status.value == "FAIL": score -= 20
        elif item.status.value == "WARNING": score -= 5
    return max(0.0, score)

def classify_promotion_eligibility(score: Optional[float], risk_flags: list[GovernanceRiskFlag]) -> PromotionEligibility:
    if score is None: return PromotionEligibility.INSUFFICIENT_DATA
    if any(f in risk_flags for f in [GovernanceRiskFlag.SECRET_LEAK_RISK, GovernanceRiskFlag.ORDER_ROUTING_RISK, GovernanceRiskFlag.CONFIG_MUTATION_RISK]):
        return PromotionEligibility.BLOCKED
    if score >= 80: return PromotionEligibility.ELIGIBLE
    if score >= 50: return PromotionEligibility.CONDITIONALLY_ELIGIBLE
    return PromotionEligibility.NOT_ELIGIBLE

def promotion_decision_from_eligibility(eligibility: PromotionEligibility, risk_flags: list[GovernanceRiskFlag], evidence_status: EvidencePackStatus) -> PromotionDecision:
    if eligibility == PromotionEligibility.BLOCKED: return PromotionDecision.BLOCK
    if evidence_status == EvidencePackStatus.MISSING_REQUIRED_EVIDENCE: return PromotionDecision.REQUEST_MORE_DATA
    if eligibility == PromotionEligibility.ELIGIBLE: return PromotionDecision.ACCEPT_AS_LOCAL_RESEARCH_CANDIDATE
    if eligibility == PromotionEligibility.CONDITIONALLY_ELIGIBLE: return PromotionDecision.APPROVE_FOR_MORE_RESEARCH
    return PromotionDecision.REJECT

def eligibility_score_components(evidence_pack: GovernanceEvidencePack, checklist_items: list[GovernanceChecklistItem]) -> dict[str, Optional[float]]:
    return {"total_score": calculate_promotion_eligibility_score(evidence_pack, checklist_items)}

def eligibility_scoring_to_text(payload: dict[str, Any]) -> str:
    return f"Eligibility: {payload}"
