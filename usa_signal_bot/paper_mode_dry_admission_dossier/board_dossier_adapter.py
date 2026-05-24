from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionDossierFullReview

def dry_admission_dossier_evidence_from_board_dossier(payload: dict[str, Any]) -> list[str]:
    return [payload.get("board_dossier_id")] if payload.get("board_dossier_id") else []

def board_dossier_supports_dry_admission_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if not payload.get("board_dossier_id"):
        reasons.append("No board dossier id")
    return len(reasons) == 0, reasons

def attach_dry_admission_dossier_hint_to_board_dossier_payload(payload: dict[str, Any], review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    payload["dry_admission_dossier_hint"] = review.review_id
    return payload

def board_dossier_dry_admission_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"hint": payload.get("dry_admission_dossier_hint")}

def board_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = board_dossier_dry_admission_summary(payload)
    return f"Board Dossier Adapter: {summary}"
