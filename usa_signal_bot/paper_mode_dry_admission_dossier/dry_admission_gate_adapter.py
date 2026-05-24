from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionGateDossier, DryAdmissionAcceptanceSeal, PaperModeRehearsalBlockerEvent, DryAdmissionDossierFullReview
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier import build_dry_admission_gate_dossier
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_report import build_dry_admission_dossier_full_review

def dry_admission_dossier_from_gate(payload: dict[str, Any]) -> DryAdmissionGateDossier:
    return build_dry_admission_gate_dossier(payload)

def dry_admission_acceptance_seal_from_gate(payload: dict[str, Any]) -> DryAdmissionAcceptanceSeal:
    return build_dry_admission_gate_dossier(payload).acceptance_seal

def rehearsal_blocker_events_from_gate(payload: dict[str, Any]) -> list[PaperModeRehearsalBlockerEvent]:
    return build_dry_admission_gate_dossier(payload).rehearsal_blocker_events

def dry_admission_dossier_full_review_from_gate(payload: dict[str, Any]) -> DryAdmissionDossierFullReview:
    return build_dry_admission_dossier_full_review(payload)

def attach_dry_admission_dossier_metadata_to_gate_payload(payload: dict[str, Any], review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    payload["dry_admission_dossier_review_id"] = review.review_id
    payload["dry_admission_dossier_metadata"] = {
        "status": review.dossiers[0].status.value if review.dossiers else "UNKNOWN",
        "seal_sealed": review.acceptance_seals[0].sealed if review.acceptance_seals else False
    }
    return payload

def dry_admission_gate_dossier_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("dry_admission_dossier_metadata", {})

def dry_admission_gate_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = dry_admission_gate_dossier_summary(payload)
    return f"Gate Adapter: {summary}"
