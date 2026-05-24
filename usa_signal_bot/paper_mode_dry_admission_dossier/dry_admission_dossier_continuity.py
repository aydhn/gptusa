from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionGateDossier, DryAdmissionAcceptanceSeal, PaperModeRehearsalBlockerEvent
from usa_signal_bot.core.enums import DryAdmissionDossierRiskFlag

def validate_dry_admission_dossier_continuity(
    dossier: DryAdmissionGateDossier | None = None,
    seal: DryAdmissionAcceptanceSeal | None = None,
    blocker_events: list[PaperModeRehearsalBlockerEvent] | None = None
) -> list[str]:
    errors = []

    if dossier:
        if not dossier.activation_denied: errors.append("Dossier activation not denied")
        if dossier.activation_allowed: errors.append("Dossier allows activation")
        if dossier.admission_allowed: errors.append("Dossier allows admission")
        if dossier.transition_allowed: errors.append("Dossier allows transition")
        if dossier.shadow_launch_allowed: errors.append("Dossier allows shadow launch")
        if dossier.paper_mode_launch_allowed: errors.append("Dossier allows paper mode launch")
        if dossier.rehearsal_allowed: errors.append("Dossier allows rehearsal")
        if dossier.paper_mode_rehearsal_allowed: errors.append("Dossier allows paper mode rehearsal")
        if not dossier.all_writes_blocked: errors.append("Dossier writes not all blocked")
        if dossier.order_created: errors.append("Dossier order created")
        if dossier.mutation_detected: errors.append("Dossier mutation detected")
        if dossier.allows_active_paper: errors.append("Dossier allows active paper")
        if dossier.allows_broker_execution: errors.append("Dossier allows broker execution")

    if seal:
        if not seal.sealed or not seal.immutable: errors.append("Seal not valid")
        if seal.allows_rehearsal or seal.allows_paper_mode_rehearsal: errors.append("Seal allows rehearsal")

    if blocker_events:
        if any(not e.blocked for e in blocker_events): errors.append("Not all rehearsal attempts blocked")

    return errors

def dry_admission_dossier_continuity_flags(payload: dict[str, Any]) -> list[DryAdmissionDossierRiskFlag]:
    flags = []
    if payload.get("activation_allowed"): flags.append(DryAdmissionDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed"): flags.append(DryAdmissionDossierRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed"): flags.append(DryAdmissionDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    return flags

def dry_admission_dossier_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    flags = dry_admission_dossier_continuity_flags(payload)
    return len(flags) == 0

def dry_admission_dossier_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    flags = dry_admission_dossier_continuity_flags(payload)
    return {
        "preserved": len(flags) == 0,
        "flags": [f.value for f in flags]
    }

def dry_admission_dossier_continuity_to_text(payload: dict[str, Any]) -> str:
    summary = dry_admission_dossier_continuity_summary(payload)
    return f"Dossier Continuity: {'PRESERVED' if summary['preserved'] else 'BROKEN'}"
