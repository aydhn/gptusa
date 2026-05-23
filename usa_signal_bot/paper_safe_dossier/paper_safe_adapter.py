from typing import Any, Dict, List
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PaperSafeGateDossier, NonExecutionAcceptanceSeal, PrePaperLocalRuntimeMap, PaperSafeDossierFullReview
from usa_signal_bot.paper_safe_dossier.dossier_report import build_paper_safe_dossier_full_review

def paper_safe_dossier_from_paper_safe_gate(payload: Dict[str, Any]) -> PaperSafeGateDossier:
    review = build_paper_safe_dossier_full_review(payload)
    return review.dossiers[0]

def non_execution_seal_from_paper_safe_gate(payload: Dict[str, Any]) -> NonExecutionAcceptanceSeal:
    review = build_paper_safe_dossier_full_review(payload)
    return review.non_execution_seals[0]

def runtime_map_from_paper_safe_gate(payload: Dict[str, Any]) -> PrePaperLocalRuntimeMap:
    review = build_paper_safe_dossier_full_review(payload)
    return review.runtime_maps[0]

def paper_safe_dossier_full_review_from_paper_safe_gate(payload: Dict[str, Any]) -> PaperSafeDossierFullReview:
    return build_paper_safe_dossier_full_review(payload)

def attach_paper_safe_dossier_metadata_to_paper_safe_payload(payload: Dict[str, Any], review: PaperSafeDossierFullReview) -> Dict[str, Any]:
    payload["paper_safe_dossier_review_id"] = review.review_id
    payload["paper_safe_dossier_status"] = review.dossiers[0].status.value if review.dossiers else "UNKNOWN"
    payload["non_execution_seal_status"] = review.non_execution_seals[0].status.value if review.non_execution_seals else "UNKNOWN"
    return payload

def paper_safe_gate_dossier_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "review_id": payload.get("paper_safe_dossier_review_id"),
        "status": payload.get("paper_safe_dossier_status")
    }

def paper_safe_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"Adapter attached Review ID: {payload.get('paper_safe_dossier_review_id')}"
