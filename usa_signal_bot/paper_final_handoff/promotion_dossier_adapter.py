from typing import Any, Dict, List, Tuple
from usa_signal_bot.paper_final_handoff.final_handoff_models import FinalHandoffEvidenceRef, FinalHandoffFullReview, create_final_handoff_evidence_ref_id, _ts

def final_handoff_evidence_from_promotion_dossier(payload: Dict[str, Any]) -> List[FinalHandoffEvidenceRef]:
    return [FinalHandoffEvidenceRef(
        evidence_ref_id=create_final_handoff_evidence_ref_id(),
        created_at_utc=_ts(),
        source_type="promotion_dossier",
        source_id=payload.get("dossier_id"),
        source_path=None,
        required=True,
        available=True,
        stale=False,
        summary={},
        warnings=[],
        errors=[]
    )]

def promotion_dossier_supports_final_handoff(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_final_handoff_hint_to_promotion_dossier(payload: Dict[str, Any], review: FinalHandoffFullReview) -> Dict[str, Any]:
    out = payload.copy()
    out["final_handoff_hint"] = review.review_id
    return out

def promotion_dossier_final_handoff_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"dossier": payload.get("dossier_id")}

def promotion_dossier_adapter_to_text(payload: Dict[str, Any]) -> str:
    return "PromotionDossierAdapter"
