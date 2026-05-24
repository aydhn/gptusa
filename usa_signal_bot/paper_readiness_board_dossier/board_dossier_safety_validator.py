from typing import Any
from usa_signal_bot.core.enums import BoardDossierRiskFlag
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    PaperReadinessBoardDossier,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerEvent
)

def collect_board_dossier_safety_flags(dossier: PaperReadinessBoardDossier | None = None, seal: AcceptanceBoardSeal | None = None, blocker_events: list[ShadowLaunchBlockerEvent] | None = None) -> list[BoardDossierRiskFlag]:
    flags = set()

    if dossier:
        flags.update(dossier.safety_flags)
        if dossier.allows_active_paper:
            flags.add(BoardDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if dossier.allows_broker_execution:
            flags.add(BoardDossierRiskFlag.BROKER_ORDER_RISK)
        if dossier.allows_paper_state_mutation:
            flags.add(BoardDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
        if dossier.allows_config_patch:
            flags.add(BoardDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
        if dossier.allows_telegram_real_send:
            flags.add(BoardDossierRiskFlag.TELEGRAM_REAL_SEND_RISK)

    if seal:
        flags.update(seal.risk_flags)
        if seal.allows_shadow_launch or seal.allows_paper_mode_launch:
            flags.add(BoardDossierRiskFlag.SHADOW_LAUNCH_RISK)

    if blocker_events:
        for event in blocker_events:
            flags.update(event.risk_flags)
            if not event.blocked:
                flags.add(BoardDossierRiskFlag.SHADOW_LAUNCH_ATTEMPT_NOT_BLOCKED)

    return list(flags)

def board_dossier_has_blocking_flags(flags: list[BoardDossierRiskFlag]) -> bool:
    blocking_flags = {
        BoardDossierRiskFlag.REAL_ORDER_RISK,
        BoardDossierRiskFlag.PAPER_ORDER_RISK,
        BoardDossierRiskFlag.BROKER_ORDER_RISK,
        BoardDossierRiskFlag.PAPER_STATE_MUTATION_RISK,
        BoardDossierRiskFlag.TELEGRAM_REAL_SEND_RISK,
        BoardDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        BoardDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        BoardDossierRiskFlag.SHADOW_LAUNCH_RISK,
        BoardDossierRiskFlag.PAPER_MODE_LAUNCH_RISK,
        BoardDossierRiskFlag.ADMISSION_ALLOWED_RISK,
        BoardDossierRiskFlag.ACTIVATION_ALLOWED_RISK,
        BoardDossierRiskFlag.TRANSITION_ALLOWED_RISK,
        BoardDossierRiskFlag.ORDER_CREATED_RISK,
        BoardDossierRiskFlag.MUTATION_DETECTED_RISK,
        BoardDossierRiskFlag.SHADOW_LAUNCH_BLOCKER_FAILED,
        BoardDossierRiskFlag.SHADOW_LAUNCH_ATTEMPT_NOT_BLOCKED,
        BoardDossierRiskFlag.SECRET_RISK
    }
    return any(f in blocking_flags for f in flags)

def validate_board_dossier_safety(dossier: PaperReadinessBoardDossier | None = None, seal: AcceptanceBoardSeal | None = None, blocker_events: list[ShadowLaunchBlockerEvent] | None = None) -> list[str]:
    issues = []
    flags = collect_board_dossier_safety_flags(dossier, seal, blocker_events)

    if board_dossier_has_blocking_flags(flags):
        for f in flags:
            issues.append(f"Blocking risk flag detected: {f.name}")

    return issues

def board_dossier_safety_summary(flags: list[BoardDossierRiskFlag]) -> dict[str, Any]:
    return {
        "is_safe": not board_dossier_has_blocking_flags(flags),
        "blocking_flag_count": sum(1 for f in flags if board_dossier_has_blocking_flags([f])),
        "total_flag_count": len(flags),
        "flags": [f.name for f in flags]
    }

def board_dossier_safety_validator_to_text(payload: dict[str, Any]) -> str:
    lines = [f"Safety Validator (Safe: {payload.get('is_safe')})"]
    if payload.get("flags"):
        lines.append("  Detected Flags:")
        for f in payload.get("flags", []):
            lines.append(f"    - {f}")
    return "\n".join(lines)
