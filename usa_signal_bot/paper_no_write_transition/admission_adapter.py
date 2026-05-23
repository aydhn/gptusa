from typing import Any
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    NoWriteTransitionDossier,
    AdmissionEvidenceSealValidation,
    PaperSandboxBridgeEnvelope,
    NoWriteTransitionFullReview
)

def transition_dossier_from_admission_review(payload: dict[str, Any]) -> NoWriteTransitionDossier:
    from usa_signal_bot.paper_no_write_transition.transition_dossier import build_no_write_transition_dossier
    return build_no_write_transition_dossier(payload)

def seal_validation_from_admission_review(payload: dict[str, Any]) -> AdmissionEvidenceSealValidation:
    from usa_signal_bot.paper_no_write_transition.evidence_seal_validator import validate_admission_evidence_seal_from_payload
    return validate_admission_evidence_seal_from_payload(payload)

def sandbox_bridge_from_admission_review(payload: dict[str, Any]) -> PaperSandboxBridgeEnvelope:
    from usa_signal_bot.paper_no_write_transition.sandbox_bridge_envelope import build_paper_sandbox_bridge_envelope
    return build_paper_sandbox_bridge_envelope(candidate_id=payload.get("candidate_id"))

def no_write_transition_full_review_from_admission_review(payload: dict[str, Any]) -> NoWriteTransitionFullReview:
    from usa_signal_bot.paper_no_write_transition.transition_report import build_no_write_transition_full_review
    return build_no_write_transition_full_review(payload)

def attach_transition_metadata_to_admission_payload(payload: dict[str, Any], review: NoWriteTransitionFullReview) -> dict[str, Any]:
    out = payload.copy()
    out["no_write_transition_review_id"] = review.review_id
    out["transition_dossier_status"] = review.dossiers[0].status.value if review.dossiers else "N/A"
    return out

def admission_transition_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "Adapter OK"}

def admission_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Admission Adapter Summary"
