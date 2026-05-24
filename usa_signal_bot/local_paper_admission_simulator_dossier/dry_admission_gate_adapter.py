from typing import Any
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import SimulatorDossierFullReview

def simulator_dossier_evidence_from_dry_admission_gate(payload: dict[str, Any]) -> list[str]:
    return [payload.get("gate_id")] if payload.get("gate_id") else []

def dry_admission_gate_supports_simulator_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if payload.get("status") not in ["VALIDATED_SAFE"]:
        reasons.append(f"Invalid status for support: {payload.get('status')}")
    if payload.get("activation_allowed"):
        reasons.append("activation_allowed is true")

    if reasons:
        return False, reasons
    return True, ["Supports simulator dossier"]

def attach_simulator_dossier_hint_to_dry_admission_gate_payload(payload: dict[str, Any], review: SimulatorDossierFullReview) -> dict[str, Any]:
    output = payload.copy()
    output["simulator_dossier_review_id_hint"] = review.review_id
    return output

def dry_admission_gate_simulator_dossier_summary(payload: dict[str, Any]) -> dict[str, Any]:
    supports, _ = dry_admission_gate_supports_simulator_dossier(payload)
    return {
        "supports_simulator_dossier": supports,
        "evidence_refs": simulator_dossier_evidence_from_dry_admission_gate(payload)
    }

def dry_admission_gate_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = dry_admission_gate_simulator_dossier_summary(payload)
    return f"--- Dry Admission Gate Adapter ---\nSupports: {summary['supports_simulator_dossier']}\nEvidence Refs: {summary['evidence_refs']}"
