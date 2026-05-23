from typing import Any
import json
from usa_signal_bot.core.enums import NoOrderDossierRiskFlag
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderPaperSessionDossier,
    BridgeReplayAuditSeal,
    PaperAdmissionBlockerEvent
)
from usa_signal_bot.paper_no_order_dossier.no_order_continuity import validate_no_order_dossier_continuity

def collect_paper_admission_safety_flags(
    dossier: NoOrderPaperSessionDossier | None = None,
    seal: BridgeReplayAuditSeal | None = None,
    blocker_events: list[PaperAdmissionBlockerEvent] | None = None
) -> list[NoOrderDossierRiskFlag]:
    flags = set()
    if dossier:
        for f in dossier.safety_flags:
            flags.add(f)
    if seal:
        for f in seal.risk_flags:
            flags.add(f)
    if blocker_events:
        for e in blocker_events:
            for f in e.risk_flags:
                flags.add(f)

    # Basic continuity flags
    reasons = validate_no_order_dossier_continuity(dossier, seal, blocker_events)
    if reasons:
        flags.add(NoOrderDossierRiskFlag.PAPER_ADMISSION_RISK)

    return list(flags)

def paper_admission_has_blocking_flags(flags: list[NoOrderDossierRiskFlag]) -> bool:
    # Any flag other than MISSING/STALE evidence is blocking
    blocking = [f for f in flags if f not in [
        NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_MISSING,
        NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_STALE
    ]]
    return len(blocking) > 0

def validate_paper_admission_safety(
    dossier: NoOrderPaperSessionDossier | None = None,
    seal: BridgeReplayAuditSeal | None = None,
    blocker_events: list[PaperAdmissionBlockerEvent] | None = None
) -> list[str]:
    reasons = validate_no_order_dossier_continuity(dossier, seal, blocker_events)
    flags = collect_paper_admission_safety_flags(dossier, seal, blocker_events)
    if paper_admission_has_blocking_flags(flags):
        reasons.append(f"Blocking flags present: {flags}")
    return reasons

def paper_admission_safety_summary(flags: list[NoOrderDossierRiskFlag]) -> dict[str, Any]:
    return {
        "safe": not paper_admission_has_blocking_flags(flags),
        "blocking_flags": [f.value for f in flags if f not in [
            NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_MISSING,
            NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_STALE
        ]],
        "warning_flags": [f.value for f in flags if f in [
            NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_MISSING,
            NoOrderDossierRiskFlag.DOSSIER_EVIDENCE_STALE
        ]]
    }

def paper_admission_safety_validator_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
