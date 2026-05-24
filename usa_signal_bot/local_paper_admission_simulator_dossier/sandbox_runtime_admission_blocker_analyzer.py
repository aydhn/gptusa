from typing import Any
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import PaperSandboxRuntimeAdmissionBlockerEvent

def sandbox_runtime_admission_blocker_all_attempts_blocked(events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> bool:
    if not events:
        return False
    return all(e.blocked for e in events)

def sandbox_runtime_admission_blocker_has_unblocked_attempts(events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> bool:
    return any(not e.blocked for e in events)

def sandbox_runtime_admission_blocker_requires_followup(events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> bool:
    return sandbox_runtime_admission_blocker_has_unblocked_attempts(events)

def sandbox_runtime_admission_blocker_followups(events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> list[str]:
    unblocked = [e.attempt_type.value for e in events if not e.blocked]
    if unblocked:
        return [f"Review unblocked attempts: {', '.join(unblocked)}"]
    return []

def sandbox_runtime_admission_blocker_risk_summary(events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> dict[str, Any]:
    return {
        "all_blocked": sandbox_runtime_admission_blocker_all_attempts_blocked(events),
        "unblocked_count": len([e for e in events if not e.blocked]),
        "has_risks": sandbox_runtime_admission_blocker_has_unblocked_attempts(events)
    }

def analyze_sandbox_runtime_admission_blocker_events(events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> dict[str, Any]:
    summary = sandbox_runtime_admission_blocker_risk_summary(events)
    followups = sandbox_runtime_admission_blocker_followups(events)
    return {
        "summary": summary,
        "followups": followups
    }

def sandbox_runtime_admission_blocker_analyzer_to_text(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    followups = payload.get("followups", [])
    lines = [
        "--- Sandbox Runtime Admission Blocker Analysis ---",
        f"All Blocked: {summary.get('all_blocked')}",
        f"Unblocked Count: {summary.get('unblocked_count')}",
        "Followups:"
    ]
    if followups:
        lines.extend([f"  - {f}" for f in followups])
    else:
        lines.append("  - None")
    return "\n".join(lines)
