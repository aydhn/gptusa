from typing import Any
from usa_signal_bot.core.enums import LocalPaperAdmissionSimulatorGateDecision, LocalPaperAdmissionSimulatorGateStatus, SimulatorGateRiskFlag

def evaluate_simulator_gate_eligibility(payload: dict[str, Any]) -> LocalPaperAdmissionSimulatorGateDecision:
    if payload.get("rehearsal_allowed") or payload.get("paper_mode_rehearsal_allowed"):
        return LocalPaperAdmissionSimulatorGateDecision.BLOCK
    if payload.get("missing_evidence"):
        return LocalPaperAdmissionSimulatorGateDecision.REQUEST_DRY_ADMISSION_EVIDENCE_FREEZE
    if payload.get("missing_rehearsal"):
        return LocalPaperAdmissionSimulatorGateDecision.REQUEST_REHEARSAL_REPLAY
    return LocalPaperAdmissionSimulatorGateDecision.PASS_TO_SIMULATOR_GATE_DOSSIER

def simulator_gate_eligibility_reasons(payload: dict[str, Any]) -> list[str]:
    return []

def simulator_gate_safety_flags_from_payload(payload: dict[str, Any]) -> list[SimulatorGateRiskFlag]:
    return []

def simulator_gate_status_from_decision(decision: LocalPaperAdmissionSimulatorGateDecision) -> LocalPaperAdmissionSimulatorGateStatus:
    return LocalPaperAdmissionSimulatorGateStatus.CREATED

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    return ""
