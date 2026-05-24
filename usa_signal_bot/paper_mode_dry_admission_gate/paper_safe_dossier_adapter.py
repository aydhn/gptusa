from typing import Any, Tuple, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import DryAdmissionGateFullReview

def dry_admission_evidence_from_paper_safe_dossier(payload: dict[str, Any]) -> List[str]:
    return ["paper_safe_dossier"] if payload else []

def paper_safe_dossier_supports_dry_admission_gate(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    if not payload:
        return False, ["Missing payload"]
    return True, []

def attach_dry_admission_hint_to_paper_safe_dossier_payload(payload: dict[str, Any], review: DryAdmissionGateFullReview) -> dict[str, Any]:
    from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_report import dry_admission_gate_full_review_summary
    new_payload = payload.copy()
    new_payload["dry_admission_hint"] = dry_admission_gate_full_review_summary(review)
    return new_payload

def paper_safe_dossier_dry_admission_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("dry_admission_hint", {})

def paper_safe_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = paper_safe_dossier_dry_admission_summary(payload)
    return f"Paper Safe Dossier Adapter Summary: {summary}"
