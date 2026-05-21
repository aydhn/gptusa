from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PromotionDossierDecision, PromotionDossierStatus, PromotionDossierRiskFlag
from .dossier_models import ObserverPromotionDossier, PromotionEvidenceIndex, create_observer_promotion_dossier_id
from .eligibility_checker import evaluate_promotion_dossier_eligibility, dossier_status_from_decision, promotion_safety_flags_from_observer_governance
from .evidence_index import build_promotion_evidence_index
from .observer_governance_ingestion import extract_observer_governance_candidate_id, extract_observer_governance_decision

def build_promotion_dossier_from_observer_governance(payload: Dict[str, Any]) -> ObserverPromotionDossier:
    candidate_id = extract_observer_governance_candidate_id(payload)
    decision = evaluate_promotion_dossier_eligibility(payload)
    evidence_index = build_promotion_evidence_index(payload)

    dossier = build_promotion_dossier(candidate_id, decision, evidence_index)
    dossier.source_observer_governance_review_id = payload.get("review_id")
    dossier.source_observer_governance_decision = extract_observer_governance_decision(payload)

    # Add safety flags from governance
    flags = promotion_safety_flags_from_observer_governance(payload)
    for f in flags:
        if f not in dossier.safety_flags:
            dossier.safety_flags.append(f)

    # Add missing/stale risk flags
    if evidence_index.missing_evidence_types:
        dossier.safety_flags.append(PromotionDossierRiskFlag.EVIDENCE_MISSING)
    if evidence_index.stale_evidence_types:
        dossier.safety_flags.append(PromotionDossierRiskFlag.EVIDENCE_STALE)

    dossier.warnings.extend(validate_promotion_dossier_safety(dossier))
    return dossier

def build_promotion_dossier(candidate_id: Optional[str], decision: PromotionDossierDecision, evidence_index: Optional[PromotionEvidenceIndex] = None) -> ObserverPromotionDossier:
    status = dossier_status_from_decision(decision)
    if status == PromotionDossierStatus.ELIGIBLE:
        status = PromotionDossierStatus.CREATED

    return ObserverPromotionDossier(
        dossier_id=create_observer_promotion_dossier_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        candidate_id=candidate_id,
        source_observer_governance_review_id=None,
        source_observer_governance_decision=None,
        evidence_index=evidence_index,
        decision=decision,
        safety_flags=[],
        manual_review_required=True,
        final_safety_board_required=True,
        allowed_for_active_paper=False,
        allowed_for_broker_execution=False,
        allowed_for_paper_state_mutation=False,
        allowed_for_config_patch=False,
        warnings=[],
        errors=[]
    )

def validate_promotion_dossier_safety(dossier: ObserverPromotionDossier) -> List[str]:
    warnings = []
    if dossier.allowed_for_active_paper: warnings.append("Dossier illegally enabled active paper.")
    if dossier.allowed_for_broker_execution: warnings.append("Dossier illegally enabled broker execution.")
    if dossier.allowed_for_paper_state_mutation: warnings.append("Dossier illegally enabled paper state mutation.")
    if dossier.allowed_for_config_patch: warnings.append("Dossier illegally enabled config patch.")
    return warnings

def promotion_dossier_summary(dossier: ObserverPromotionDossier) -> Dict[str, Any]:
    return {
        "dossier_id": dossier.dossier_id,
        "status": dossier.status.value,
        "candidate_id": dossier.candidate_id,
        "decision": dossier.decision.value,
        "safety_flags_count": len(dossier.safety_flags),
        "allowed_for_active_paper": dossier.allowed_for_active_paper
    }

def promotion_dossier_to_text(dossier: ObserverPromotionDossier) -> str:
    return f"Dossier {dossier.dossier_id} for Candidate {dossier.candidate_id}. Status: {dossier.status.value}."
