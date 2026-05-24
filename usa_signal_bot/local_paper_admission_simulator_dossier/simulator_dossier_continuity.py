from typing import Any
from usa_signal_bot.core.enums import SimulatorDossierRiskFlag, SimulatorAcceptanceSealStatus
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorAcceptanceSeal,
    PaperSandboxRuntimeAdmissionBlockerEvent
)

def simulator_dossier_continuity_flags(payload: dict[str, Any]) -> list[SimulatorDossierRiskFlag]:
    flags = []
    if not payload.get("activation_denied", True): flags.append(SimulatorDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("activation_allowed"): flags.append(SimulatorDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed"): flags.append(SimulatorDossierRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed"): flags.append(SimulatorDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("simulator_admission_allowed"): flags.append(SimulatorDossierRiskFlag.SIMULATED_ADMISSION_RISK)
    if payload.get("local_paper_simulator_allowed"): flags.append(SimulatorDossierRiskFlag.LOCAL_PAPER_SIMULATOR_RISK)
    if payload.get("sandbox_runtime_admission_allowed"): flags.append(SimulatorDossierRiskFlag.SANDBOX_RUNTIME_ADMISSION_RISK)
    if payload.get("paper_sandbox_runtime_allowed"): flags.append(SimulatorDossierRiskFlag.PAPER_SANDBOX_RUNTIME_RISK)
    if payload.get("rehearsal_allowed"): flags.append(SimulatorDossierRiskFlag.PAPER_MODE_REHEARSAL_RISK)
    if not payload.get("all_writes_blocked", True): flags.append(SimulatorDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("order_created"): flags.append(SimulatorDossierRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected"): flags.append(SimulatorDossierRiskFlag.MUTATION_DETECTED_RISK)
    return flags

def simulator_dossier_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    flags = simulator_dossier_continuity_flags(payload)
    return len(flags) == 0

def validate_simulator_dossier_continuity(
    dossier: LocalPaperAdmissionSimulatorGateDossier | None = None,
    seal: SimulatorAcceptanceSeal | None = None,
    blocker_events: list[PaperSandboxRuntimeAdmissionBlockerEvent] | None = None
) -> list[str]:
    errors = []
    if dossier:
        if not dossier.activation_denied: errors.append("activation_denied is false")
        if dossier.activation_allowed: errors.append("activation_allowed is true")
        if dossier.admission_allowed: errors.append("admission_allowed is true")
        if dossier.transition_allowed: errors.append("transition_allowed is true")
        if dossier.sandbox_runtime_admission_allowed: errors.append("sandbox_runtime_admission_allowed is true")
        if dossier.paper_sandbox_runtime_allowed: errors.append("paper_sandbox_runtime_allowed is true")
        if not dossier.all_writes_blocked: errors.append("all_writes_blocked is false")
        if dossier.order_created: errors.append("order_created is true")
        if dossier.mutation_detected: errors.append("mutation_detected is true")
    if seal:
        if seal.status != SimulatorAcceptanceSealStatus.SEALED:
            errors.append(f"Simulator acceptance seal status is {seal.status.value}")
    if blocker_events:
        for e in blocker_events:
            if not e.blocked:
                errors.append(f"Blocker event {e.attempt_type.value} is not blocked")
    return errors

def simulator_dossier_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    flags = simulator_dossier_continuity_flags(payload)
    return {
        "is_preserved": simulator_dossier_continuity_is_preserved(payload),
        "flags": [f.value for f in flags]
    }

def simulator_dossier_continuity_to_text(payload: dict[str, Any]) -> str:
    summary = simulator_dossier_continuity_summary(payload)
    lines = [
        "--- Simulator Dossier Continuity ---",
        f"Preserved: {summary['is_preserved']}",
        "Flags:"
    ]
    if summary["flags"]:
        lines.extend([f"  - {f}" for f in summary["flags"]])
    else:
        lines.append("  - None")
    return "\n".join(lines)
