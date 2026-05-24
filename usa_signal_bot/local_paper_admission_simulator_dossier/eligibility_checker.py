from typing import Any
from usa_signal_bot.core.enums import (
    LocalPaperAdmissionSimulatorDossierDecision,
    LocalPaperAdmissionSimulatorDossierStatus,
    SimulatorDossierRiskFlag
)
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_gate_ingestion import (
    simulator_gate_supports_dossier,
    extract_final_simulator_gate,
    extract_rehearsal_replay_result,
    extract_dry_admission_evidence_freeze
)

def simulator_dossier_safety_flags_from_payload(payload: dict[str, Any]) -> list[SimulatorDossierRiskFlag]:
    flags = []
    if payload.get("order_created"): flags.append(SimulatorDossierRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected"): flags.append(SimulatorDossierRiskFlag.MUTATION_DETECTED_RISK)
    if payload.get("activation_allowed"): flags.append(SimulatorDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed"): flags.append(SimulatorDossierRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed"): flags.append(SimulatorDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("simulator_admission_allowed"): flags.append(SimulatorDossierRiskFlag.SIMULATED_ADMISSION_RISK)
    if payload.get("local_paper_simulator_allowed"): flags.append(SimulatorDossierRiskFlag.LOCAL_PAPER_SIMULATOR_RISK)
    if payload.get("paper_sandbox_runtime_allowed"): flags.append(SimulatorDossierRiskFlag.PAPER_SANDBOX_RUNTIME_RISK)
    if payload.get("sandbox_runtime_admission_allowed"): flags.append(SimulatorDossierRiskFlag.SANDBOX_RUNTIME_ADMISSION_RISK)
    return flags

def simulator_dossier_eligibility_reasons(payload: dict[str, Any]) -> list[str]:
    reasons = []
    supports, gate_reasons = simulator_gate_supports_dossier(payload)
    if not supports:
        reasons.extend(gate_reasons)

    if payload.get("manual_review_required") is False:
        reasons.append("Manual review not required")

    flags = simulator_dossier_safety_flags_from_payload(payload)
    if flags:
        reasons.extend([f.value for f in flags])

    return reasons

def evaluate_simulator_dossier_eligibility(payload: dict[str, Any]) -> LocalPaperAdmissionSimulatorDossierDecision:
    reasons = simulator_dossier_eligibility_reasons(payload)
    flags = simulator_dossier_safety_flags_from_payload(payload)

    if flags:
        return LocalPaperAdmissionSimulatorDossierDecision.BLOCK

    gate = extract_final_simulator_gate(payload)
    if not gate or gate.get("status") in ["FAILED", "STALE"]:
        return LocalPaperAdmissionSimulatorDossierDecision.REQUEST_SIMULATOR_GATE_REFRESH

    replay = extract_rehearsal_replay_result(payload)
    if not replay or replay.get("status") in ["FAILED"]:
        return LocalPaperAdmissionSimulatorDossierDecision.REQUEST_SIMULATOR_GATE_REFRESH

    freeze = extract_dry_admission_evidence_freeze(payload)
    if not freeze or freeze.get("status") in ["FAILED", "STALE"]:
        return LocalPaperAdmissionSimulatorDossierDecision.REQUEST_SIMULATOR_GATE_REFRESH

    if payload.get("manual_review_missing", False):
        return LocalPaperAdmissionSimulatorDossierDecision.REQUEST_MANUAL_REVIEW

    if payload.get("reject", False):
        return LocalPaperAdmissionSimulatorDossierDecision.REJECT

    if not reasons:
        return LocalPaperAdmissionSimulatorDossierDecision.CREATE_SIMULATOR_DOSSIER

    return LocalPaperAdmissionSimulatorDossierDecision.INCONCLUSIVE

def simulator_dossier_status_from_decision(decision: LocalPaperAdmissionSimulatorDossierDecision) -> LocalPaperAdmissionSimulatorDossierStatus:
    mapping = {
        LocalPaperAdmissionSimulatorDossierDecision.CREATE_SIMULATOR_DOSSIER: LocalPaperAdmissionSimulatorDossierStatus.VALIDATED_SIMULATOR_SAFE,
        LocalPaperAdmissionSimulatorDossierDecision.REQUEST_SIMULATOR_GATE_REFRESH: LocalPaperAdmissionSimulatorDossierStatus.REQUEST_CHANGES,
        LocalPaperAdmissionSimulatorDossierDecision.REQUEST_SIMULATOR_ACCEPTANCE_SEAL_REFRESH: LocalPaperAdmissionSimulatorDossierStatus.REQUEST_CHANGES,
        LocalPaperAdmissionSimulatorDossierDecision.REQUEST_SANDBOX_RUNTIME_ADMISSION_BLOCKER_REFRESH: LocalPaperAdmissionSimulatorDossierStatus.REQUEST_CHANGES,
        LocalPaperAdmissionSimulatorDossierDecision.REQUEST_MANUAL_REVIEW: LocalPaperAdmissionSimulatorDossierStatus.REQUEST_CHANGES,
        LocalPaperAdmissionSimulatorDossierDecision.REJECT: LocalPaperAdmissionSimulatorDossierStatus.REJECTED,
        LocalPaperAdmissionSimulatorDossierDecision.BLOCK: LocalPaperAdmissionSimulatorDossierStatus.BLOCKED,
        LocalPaperAdmissionSimulatorDossierDecision.INCONCLUSIVE: LocalPaperAdmissionSimulatorDossierStatus.UNKNOWN,
        LocalPaperAdmissionSimulatorDossierDecision.UNKNOWN: LocalPaperAdmissionSimulatorDossierStatus.UNKNOWN,
    }
    return mapping.get(decision, LocalPaperAdmissionSimulatorDossierStatus.UNKNOWN)

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_simulator_dossier_eligibility(payload)
    reasons = simulator_dossier_eligibility_reasons(payload)
    lines = [
        "--- Simulator Dossier Eligibility ---",
        f"Decision: {decision.value}",
        "Reasons:"
    ]
    if reasons:
        lines.extend([f"  - {r}" for r in reasons])
    else:
        lines.append("  - None")
    return "\n".join(lines)
