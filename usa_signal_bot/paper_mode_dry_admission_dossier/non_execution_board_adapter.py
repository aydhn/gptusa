from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionDossierFullReview

def dry_admission_dossier_evidence_from_non_execution_board(payload: dict[str, Any]) -> list[str]:
    return [payload.get("non_execution_board_id")] if payload.get("non_execution_board_id") else []

def non_execution_board_supports_dry_admission_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if not payload.get("non_execution_board_id"):
        reasons.append("No non-execution board id")
    return len(reasons) == 0, reasons

def attach_dry_admission_dossier_hint_to_non_execution_board_payload(payload: dict[str, Any], review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    payload["dry_admission_dossier_hint"] = review.review_id
    return payload

def non_execution_board_dry_admission_dossier_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"hint": payload.get("dry_admission_dossier_hint")}

def non_execution_board_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = non_execution_board_dry_admission_dossier_summary(payload)
    return f"Non-Execution Board Adapter: {summary}"
