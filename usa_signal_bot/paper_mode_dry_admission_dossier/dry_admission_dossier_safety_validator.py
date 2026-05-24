from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionGateDossier, DryAdmissionAcceptanceSeal, PaperModeRehearsalBlockerEvent
from usa_signal_bot.core.enums import DryAdmissionDossierRiskFlag

def collect_dry_admission_dossier_safety_flags(
    dossier: DryAdmissionGateDossier | None = None,
    seal: DryAdmissionAcceptanceSeal | None = None,
    blocker_events: list[PaperModeRehearsalBlockerEvent] | None = None
) -> list[DryAdmissionDossierRiskFlag]:
    flags = []

    if dossier:
        flags.extend(dossier.safety_flags)
        if dossier.activation_allowed: flags.append(DryAdmissionDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
        if dossier.allows_broker_execution: flags.append(DryAdmissionDossierRiskFlag.BROKER_ORDER_RISK)
        if dossier.allows_paper_state_mutation: flags.append(DryAdmissionDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
        if dossier.allows_telegram_real_send: flags.append(DryAdmissionDossierRiskFlag.TELEGRAM_REAL_SEND_RISK)

    if seal:
        if seal.allows_active_paper: flags.append(DryAdmissionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if seal.allows_rehearsal: flags.append(DryAdmissionDossierRiskFlag.PAPER_MODE_REHEARSAL_RISK)

    if blocker_events:
        if any(not e.blocked for e in blocker_events):
            flags.append(DryAdmissionDossierRiskFlag.REHEARSAL_ATTEMPT_NOT_BLOCKED)

    return list(set(flags))

def dry_admission_dossier_has_blocking_flags(flags: list[DryAdmissionDossierRiskFlag]) -> bool:
    return len(flags) > 0

def validate_dry_admission_dossier_safety(
    dossier: DryAdmissionGateDossier | None = None,
    seal: DryAdmissionAcceptanceSeal | None = None,
    blocker_events: list[PaperModeRehearsalBlockerEvent] | None = None
) -> list[str]:
    flags = collect_dry_admission_dossier_safety_flags(dossier, seal, blocker_events)
    return [f.value for f in flags]

def dry_admission_dossier_safety_summary(flags: list[DryAdmissionDossierRiskFlag]) -> dict[str, Any]:
    return {
        "safe": len(flags) == 0,
        "flags": [f.value for f in flags]
    }

def dry_admission_dossier_safety_validator_to_text(payload: dict[str, Any]) -> str:
    safe = payload.get("safe", False)
    return f"Dossier Safety: {'SAFE' if safe else 'UNSAFE'}"
