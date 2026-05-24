from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import PaperModeRehearsalBlockerEvent
from usa_signal_bot.core.enums import DryAdmissionDossierRiskFlag

def rehearsal_blocker_all_attempts_blocked(events: list[PaperModeRehearsalBlockerEvent]) -> bool:
    if not events:
        return False
    return all(e.blocked for e in events)

def rehearsal_blocker_has_unblocked_attempts(events: list[PaperModeRehearsalBlockerEvent]) -> bool:
    return any(not e.blocked for e in events)

def rehearsal_blocker_followups(events: list[PaperModeRehearsalBlockerEvent]) -> list[str]:
    if rehearsal_blocker_has_unblocked_attempts(events):
        return ["INVESTIGATE_UNBLOCKED_REHEARSAL_ATTEMPT"]
    return []

def rehearsal_blocker_requires_followup(events: list[PaperModeRehearsalBlockerEvent]) -> bool:
    return len(rehearsal_blocker_followups(events)) > 0

def rehearsal_blocker_risk_summary(events: list[PaperModeRehearsalBlockerEvent]) -> dict[str, Any]:
    return {
        "all_blocked": rehearsal_blocker_all_attempts_blocked(events),
        "has_unblocked": rehearsal_blocker_has_unblocked_attempts(events),
        "requires_followup": rehearsal_blocker_requires_followup(events)
    }

def analyze_rehearsal_blocker_events(events: list[PaperModeRehearsalBlockerEvent]) -> dict[str, Any]:
    return rehearsal_blocker_risk_summary(events)

def rehearsal_blocker_analyzer_to_text(payload: dict[str, Any]) -> str:
    all_blocked = payload.get("all_blocked", False)
    return f"Rehearsal Blocker Analyzer: All Blocked = {all_blocked}"
