from typing import Any
import json
from usa_signal_bot.core.enums import NoOrderDossierRiskFlag
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import PaperAdmissionBlockerEvent

def blocker_all_attempts_blocked(events: list[PaperAdmissionBlockerEvent]) -> bool:
    if not events:
        return True # Default safe if no events
    return all(e.blocked for e in events)

def blocker_has_unblocked_attempts(events: list[PaperAdmissionBlockerEvent]) -> bool:
    return any(not e.blocked for e in events)

def blocker_requires_followup(events: list[PaperAdmissionBlockerEvent]) -> bool:
    return blocker_has_unblocked_attempts(events)

def blocker_followups(events: list[PaperAdmissionBlockerEvent]) -> list[str]:
    followups = []
    if blocker_has_unblocked_attempts(events):
        followups.append("CRITICAL: Some admission attempts were not blocked")
    return followups

def blocker_risk_summary(events: list[PaperAdmissionBlockerEvent]) -> dict[str, Any]:
    flags = []
    if blocker_has_unblocked_attempts(events):
        flags.append(NoOrderDossierRiskFlag.ADMISSION_ATTEMPT_NOT_BLOCKED.value)
        flags.append(NoOrderDossierRiskFlag.PAPER_ADMISSION_RISK.value)

    return {
        "all_blocked": blocker_all_attempts_blocked(events),
        "unblocked_count": len([e for e in events if not e.blocked]),
        "risk_flags": flags
    }

def analyze_admission_blocker_events(events: list[PaperAdmissionBlockerEvent]) -> dict[str, Any]:
    return {
        "summary": blocker_risk_summary(events),
        "requires_followup": blocker_requires_followup(events),
        "followups": blocker_followups(events)
    }

def admission_blocker_analyzer_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
