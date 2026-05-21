from typing import Any, Dict, List
from usa_signal_bot.core.enums import PromotionDossierDecision, PromotionDossierStatus, PromotionDossierRiskFlag
from .observer_governance_ingestion import (
    observer_governance_supports_promotion_dossier,
    extract_observer_governance_decision,
    extract_observer_governance_risk_flags
)

def evaluate_promotion_dossier_eligibility(observer_governance_payload: Dict[str, Any]) -> PromotionDossierDecision:
    supports, _ = observer_governance_supports_promotion_dossier(observer_governance_payload)
    decision = extract_observer_governance_decision(observer_governance_payload)

    if supports:
        return PromotionDossierDecision.CREATE_DOSSIER
    if decision in ["BLOCK", "REJECT"]:
        return PromotionDossierDecision.BLOCK

    return PromotionDossierDecision.INCONCLUSIVE

def promotion_dossier_eligibility_reasons(observer_governance_payload: Dict[str, Any]) -> List[str]:
    _, reasons = observer_governance_supports_promotion_dossier(observer_governance_payload)
    if not reasons:
        reasons.append("Eligible for non-executing promotion dossier.")
    return reasons

def promotion_safety_flags_from_observer_governance(payload: Dict[str, Any]) -> List[PromotionDossierRiskFlag]:
    flags = extract_observer_governance_risk_flags(payload)
    risk_flags = []
    for f in flags:
        try:
            risk_flags.append(PromotionDossierRiskFlag(f))
        except ValueError:
            risk_flags.append(PromotionDossierRiskFlag.UNKNOWN)
    return risk_flags

def dossier_status_from_decision(decision: PromotionDossierDecision) -> PromotionDossierStatus:
    if decision == PromotionDossierDecision.CREATE_DOSSIER:
        return PromotionDossierStatus.ELIGIBLE
    if decision in [PromotionDossierDecision.BLOCK, PromotionDossierDecision.REJECT]:
        return PromotionDossierStatus.BLOCKED
    return PromotionDossierStatus.DRAFT

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    decision = evaluate_promotion_dossier_eligibility(payload)
    reasons = promotion_dossier_eligibility_reasons(payload)
    return f"Eligibility: {decision.value}. Reasons: {', '.join(reasons)}"
