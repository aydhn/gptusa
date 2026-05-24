from typing import Any
from usa_signal_bot.core.enums import SimulatorDossierRiskFlag
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorAcceptanceSeal,
    PaperSandboxRuntimeAdmissionBlockerEvent
)

def collect_simulator_dossier_safety_flags(
    dossier: LocalPaperAdmissionSimulatorGateDossier | None = None,
    seal: SimulatorAcceptanceSeal | None = None,
    blocker_events: list[PaperSandboxRuntimeAdmissionBlockerEvent] | None = None
) -> list[SimulatorDossierRiskFlag]:
    flags = set()
    if dossier:
        flags.update(dossier.safety_flags)
        if dossier.activation_allowed: flags.add(SimulatorDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
        if dossier.order_created: flags.add(SimulatorDossierRiskFlag.ORDER_CREATED_RISK)
        if dossier.mutation_detected: flags.add(SimulatorDossierRiskFlag.MUTATION_DETECTED_RISK)
    if seal:
        flags.update(seal.risk_flags)
        if seal.allows_active_paper: flags.add(SimulatorDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if blocker_events:
        for e in blocker_events:
            flags.update(e.risk_flags)
            if not e.blocked:
                flags.add(SimulatorDossierRiskFlag.SANDBOX_RUNTIME_ADMISSION_ATTEMPT_NOT_BLOCKED)
    return list(flags)

def simulator_dossier_has_blocking_flags(flags: list[SimulatorDossierRiskFlag]) -> bool:
    return len(flags) > 0

def validate_simulator_dossier_safety(
    dossier: LocalPaperAdmissionSimulatorGateDossier | None = None,
    seal: SimulatorAcceptanceSeal | None = None,
    blocker_events: list[PaperSandboxRuntimeAdmissionBlockerEvent] | None = None
) -> list[str]:
    flags = collect_simulator_dossier_safety_flags(dossier, seal, blocker_events)
    errors = [f.value for f in flags]
    return errors

def simulator_dossier_safety_summary(flags: list[SimulatorDossierRiskFlag]) -> dict[str, Any]:
    return {
        "is_safe": not simulator_dossier_has_blocking_flags(flags),
        "flags": [f.value for f in flags]
    }

def simulator_dossier_safety_validator_to_text(payload: dict[str, Any]) -> str:
    flags_raw = payload.get("flags", [])
    try:
        flags = [SimulatorDossierRiskFlag(f) for f in flags_raw]
    except ValueError:
        flags = []
    summary = simulator_dossier_safety_summary(flags)
    lines = [
        "--- Simulator Dossier Safety Validator ---",
        f"Safe: {summary['is_safe']}",
        "Flags:"
    ]
    if summary["flags"]:
        lines.extend([f"  - {f}" for f in summary["flags"]])
    else:
        lines.append("  - None")
    return "\n".join(lines)
