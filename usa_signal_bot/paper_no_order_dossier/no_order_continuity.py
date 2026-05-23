from typing import Any
import json
from usa_signal_bot.core.enums import NoOrderDossierRiskFlag
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderPaperSessionDossier,
    BridgeReplayAuditSeal,
    PaperAdmissionBlockerEvent
)
from usa_signal_bot.paper_no_order_dossier.admission_blocker_analyzer import blocker_all_attempts_blocked
from usa_signal_bot.paper_no_order_dossier.bridge_replay_seal_validator import bridge_replay_seal_blocks_next_stage

def validate_no_order_dossier_continuity(
    dossier: NoOrderPaperSessionDossier | None = None,
    seal: BridgeReplayAuditSeal | None = None,
    blocker_events: list[PaperAdmissionBlockerEvent] | None = None
) -> list[str]:
    reasons = []

    if dossier:
        if not dossier.activation_denied:
            reasons.append("dossier activation_denied is false")
        if dossier.activation_allowed:
            reasons.append("dossier activation_allowed is true")
        if dossier.admission_allowed:
            reasons.append("dossier admission_allowed is true")
        if dossier.transition_allowed:
            reasons.append("dossier transition_allowed is true")
        if not dossier.all_writes_blocked:
            reasons.append("dossier all_writes_blocked is false")
        if dossier.order_created:
            reasons.append("dossier order_created is true")
        if dossier.mutation_detected:
            reasons.append("dossier mutation_detected is true")
        if dossier.allows_active_paper:
            reasons.append("dossier allows_active_paper is true")
        if dossier.allows_broker_execution:
            reasons.append("dossier allows_broker_execution is true")

    if seal:
        if bridge_replay_seal_blocks_next_stage(seal):
            reasons.append("seal is invalid/unsafe")

    if blocker_events is not None:
        if not blocker_all_attempts_blocked(blocker_events):
            reasons.append("not all admission attempts were blocked")

    return reasons

def no_order_dossier_continuity_flags(payload: dict[str, Any]) -> list[NoOrderDossierRiskFlag]:
    flags = []

    reasons = validate_no_order_dossier_continuity(
        payload.get("dossier"),
        payload.get("seal"),
        payload.get("blocker_events")
    )

    if any("activation_allowed" in r for r in reasons):
        flags.append(NoOrderDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if any("admission_allowed" in r for r in reasons):
        flags.append(NoOrderDossierRiskFlag.PAPER_ADMISSION_RISK)
    if any("order_created" in r for r in reasons):
        flags.append(NoOrderDossierRiskFlag.ORDER_CREATED_RISK)
    if any("mutation_detected" in r for r in reasons):
        flags.append(NoOrderDossierRiskFlag.MUTATION_DETECTED_RISK)
    if any("not all admission attempts" in r for r in reasons):
        flags.append(NoOrderDossierRiskFlag.ADMISSION_ATTEMPT_NOT_BLOCKED)

    return flags

def no_order_dossier_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    return len(validate_no_order_dossier_continuity(
        payload.get("dossier"),
        payload.get("seal"),
        payload.get("blocker_events")
    )) == 0

def no_order_dossier_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    reasons = validate_no_order_dossier_continuity(
        payload.get("dossier"),
        payload.get("seal"),
        payload.get("blocker_events")
    )
    return {
        "preserved": len(reasons) == 0,
        "reasons": reasons,
        "risk_flags": [f.value for f in no_order_dossier_continuity_flags(payload)]
    }

def no_order_dossier_continuity_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
