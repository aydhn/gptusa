from typing import Any
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    PaperReadinessBoardDossier,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerEvent
)
from usa_signal_bot.core.enums import BoardDossierRiskFlag

def validate_board_dossier_continuity(dossier: PaperReadinessBoardDossier | None = None, seal: AcceptanceBoardSeal | None = None, blocker_events: list[ShadowLaunchBlockerEvent] | None = None) -> list[str]:
    issues = []

    if dossier:
        if not dossier.activation_denied:
            issues.append("Dossier activation_denied is not True")
        if dossier.activation_allowed:
            issues.append("Dossier activation_allowed is True")
        if dossier.admission_allowed:
            issues.append("Dossier admission_allowed is True")
        if dossier.transition_allowed:
            issues.append("Dossier transition_allowed is True")
        if dossier.shadow_launch_allowed:
            issues.append("Dossier shadow_launch_allowed is True")
        if dossier.paper_mode_launch_allowed:
            issues.append("Dossier paper_mode_launch_allowed is True")
        if not dossier.all_writes_blocked:
            issues.append("Dossier all_writes_blocked is not True")
        if dossier.order_created:
            issues.append("Dossier order_created is True")
        if dossier.mutation_detected:
            issues.append("Dossier mutation_detected is True")

    if seal:
        if not seal.sealed or not seal.immutable:
            issues.append("Seal is not sealed/immutable")
        if seal.allows_shadow_launch or seal.allows_active_paper:
            issues.append("Seal allows shadow launch or active paper")

    if blocker_events:
        for event in blocker_events:
            if not event.blocked:
                issues.append(f"Blocker event {event.attempt_type.name} is not blocked")

    return issues

def board_dossier_continuity_flags(payload: dict[str, Any]) -> list[BoardDossierRiskFlag]:
    flags = []

    # Generic payload check if objects aren't passed directly
    if payload.get("activation_allowed") is True:
        flags.append(BoardDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed") is True:
        flags.append(BoardDossierRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed") is True:
        flags.append(BoardDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("shadow_launch_allowed") is True:
        flags.append(BoardDossierRiskFlag.SHADOW_LAUNCH_RISK)
    if payload.get("paper_mode_launch_allowed") is True:
        flags.append(BoardDossierRiskFlag.PAPER_MODE_LAUNCH_RISK)
    if payload.get("order_created") is True:
        flags.append(BoardDossierRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected") is True:
        flags.append(BoardDossierRiskFlag.MUTATION_DETECTED_RISK)

    return flags

def board_dossier_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    flags = board_dossier_continuity_flags(payload)
    return len(flags) == 0

def board_dossier_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    flags = board_dossier_continuity_flags(payload)
    return {
        "is_preserved": len(flags) == 0,
        "risk_flag_count": len(flags),
        "flags": [f.name for f in flags]
    }

def board_dossier_continuity_to_text(payload: dict[str, Any]) -> str:
    summary = board_dossier_continuity_summary(payload)
    lines = [f"Board Continuity (Preserved: {summary['is_preserved']})"]
    if summary["flags"]:
        lines.append("  Violations:")
        for f in summary["flags"]:
            lines.append(f"    - {f}")
    return "\n".join(lines)
