from typing import Any
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import ShadowLaunchBlockerEvent
from usa_signal_bot.core.enums import BoardDossierRiskFlag

def shadow_launch_blocker_all_attempts_blocked(events: list[ShadowLaunchBlockerEvent]) -> bool:
    if not events:
        return False
    return all(e.blocked for e in events)

def shadow_launch_blocker_has_unblocked_attempts(events: list[ShadowLaunchBlockerEvent]) -> bool:
    return any(not e.blocked for e in events)

def shadow_launch_blocker_requires_followup(events: list[ShadowLaunchBlockerEvent]) -> bool:
    if not events:
        return True
    return shadow_launch_blocker_has_unblocked_attempts(events)

def shadow_launch_blocker_followups(events: list[ShadowLaunchBlockerEvent]) -> list[str]:
    followups = []
    if not events:
        followups.append("No shadow launch attempts simulated")
    unblocked = [e.attempt_type.name for e in events if not e.blocked]
    if unblocked:
        followups.append(f"Unblocked attempts detected: {', '.join(unblocked)}")
    return followups

def shadow_launch_blocker_risk_summary(events: list[ShadowLaunchBlockerEvent]) -> dict[str, Any]:
    flags = []
    if not events or shadow_launch_blocker_has_unblocked_attempts(events):
        flags.append(BoardDossierRiskFlag.SHADOW_LAUNCH_ATTEMPT_NOT_BLOCKED.name)

    return {
        "all_blocked": shadow_launch_blocker_all_attempts_blocked(events),
        "unblocked_count": sum(1 for e in events if not e.blocked),
        "risk_flags": flags,
        "requires_followup": shadow_launch_blocker_requires_followup(events)
    }

def analyze_shadow_launch_blocker_events(events: list[ShadowLaunchBlockerEvent]) -> dict[str, Any]:
    return {
        "all_blocked": shadow_launch_blocker_all_attempts_blocked(events),
        "has_unblocked": shadow_launch_blocker_has_unblocked_attempts(events),
        "requires_followup": shadow_launch_blocker_requires_followup(events),
        "followups": shadow_launch_blocker_followups(events),
        "risk_summary": shadow_launch_blocker_risk_summary(events)
    }

def shadow_launch_blocker_analyzer_to_text(payload: dict[str, Any]) -> str:
    lines = [f"Blocker Analyzer (All Blocked: {payload.get('all_blocked')})"]
    if payload.get("has_unblocked"):
        lines.append(f"  WARNING: Unblocked attempts detected!")
    if payload.get("followups"):
        lines.append("  Followups:")
        for f in payload.get("followups", []):
            lines.append(f"    - {f}")
    return "\n".join(lines)
