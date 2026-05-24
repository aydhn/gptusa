from typing import Any
from .simulator_gate_models import FinalLocalPaperAdmissionSimulatorGate, RehearsalReplayResult, DryAdmissionEvidenceFreezeBundle, SimulatorGateFullReview

def simulator_gate_from_dry_admission_dossier(payload: dict[str, Any]) -> FinalLocalPaperAdmissionSimulatorGate:
    pass

def rehearsal_replay_result_from_dry_admission_dossier(payload: dict[str, Any]) -> RehearsalReplayResult:
    pass

def dry_admission_evidence_freeze_from_dry_admission_dossier(payload: dict[str, Any]) -> DryAdmissionEvidenceFreezeBundle:
    pass

def simulator_full_review_from_dry_admission_dossier(payload: dict[str, Any]) -> SimulatorGateFullReview:
    pass

def attach_simulator_metadata_to_dry_admission_dossier_payload(payload: dict[str, Any], review: SimulatorGateFullReview) -> dict[str, Any]:
    return payload

def dry_admission_dossier_simulator_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def dry_admission_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    return ""
