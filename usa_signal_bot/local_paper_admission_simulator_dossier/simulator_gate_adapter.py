from typing import Any
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorAcceptanceSeal,
    PaperSandboxRuntimeAdmissionBlockerEvent,
    SimulatorDossierFullReview
)
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_report import build_simulator_dossier_full_review

def simulator_dossier_from_gate(payload: dict[str, Any]) -> LocalPaperAdmissionSimulatorGateDossier:
    review = build_simulator_dossier_full_review(payload)
    return review.dossiers[0]

def simulator_acceptance_seal_from_gate(payload: dict[str, Any]) -> SimulatorAcceptanceSeal:
    review = build_simulator_dossier_full_review(payload)
    return review.acceptance_seals[0]

def sandbox_runtime_admission_blocker_events_from_gate(payload: dict[str, Any]) -> list[PaperSandboxRuntimeAdmissionBlockerEvent]:
    review = build_simulator_dossier_full_review(payload)
    return review.sandbox_runtime_admission_blocker_events

def simulator_dossier_full_review_from_gate(payload: dict[str, Any]) -> SimulatorDossierFullReview:
    return build_simulator_dossier_full_review(payload)

def attach_simulator_dossier_metadata_to_gate_payload(payload: dict[str, Any], review: SimulatorDossierFullReview) -> dict[str, Any]:
    output = payload.copy()
    output["simulator_dossier_review_id"] = review.review_id
    output["simulator_dossier_status"] = review.dossiers[0].status.value if review.dossiers else "UNKNOWN"
    return output

def simulator_gate_dossier_summary(payload: dict[str, Any]) -> dict[str, Any]:
    review = build_simulator_dossier_full_review(payload)
    return {
        "review_id": review.review_id,
        "dossier_status": review.dossiers[0].status.value if review.dossiers else "UNKNOWN"
    }

def simulator_gate_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = simulator_gate_dossier_summary(payload)
    return f"--- Simulator Gate Adapter ---\nReview ID: {summary['review_id']}\nDossier Status: {summary['dossier_status']}"
