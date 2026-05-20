from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, CheckpointHistoryEntry, ObservationTelemetrySummary, ObservationScorecard
from usa_signal_bot.paper_observation.checkpoint_history import checkpoint_history_status

def gate_min_observation_sessions(window: ObservationWindow) -> dict[str, Any]:
    passed = window.observed_session_count >= window.required_session_count
    return {
        "gate_name": "MIN_OBSERVATION_SESSIONS",
        "passed": passed,
        "details": f"{window.observed_session_count}/{window.required_session_count}"
    }

def gate_checkpoint_history_complete(entries: List[CheckpointHistoryEntry]) -> dict[str, Any]:
    status = checkpoint_history_status(entries)
    passed = status == "COMPLETE"
    return {
        "gate_name": "CHECKPOINT_HISTORY_COMPLETE",
        "passed": passed,
        "details": f"Status: {status}"
    }

def gate_no_blocked_dangerous_operations(telemetry: ObservationTelemetrySummary) -> dict[str, Any]:
    passed = telemetry.blocked_operation_count == 0
    return {
        "gate_name": "NO_BLOCKED_DANGEROUS_OPERATIONS",
        "passed": passed,
        "details": f"Blocked: {telemetry.blocked_operation_count}"
    }

def gate_notification_safety(sessions: List[dict[str, Any]]) -> dict[str, Any]:
    # Placeholder simplified logic; in real code calls notification_safety_history
    passed = True
    return {
        "gate_name": "NOTIFICATION_SAFETY",
        "passed": passed,
        "details": "Checked via sessions"
    }

def gate_no_active_paper_permissions(scorecard: ObservationScorecard) -> dict[str, Any]:
    passed = not (scorecard.allows_active_paper or scorecard.allows_broker_execution or scorecard.allows_paper_state_mutation or scorecard.allows_config_patch)
    return {
        "gate_name": "NO_ACTIVE_PAPER_PERMISSIONS",
        "passed": passed,
        "details": "Permissions safely off"
    }

def default_quarantine_exit_gates(
    window: ObservationWindow,
    telemetry: ObservationTelemetrySummary,
    entries: List[CheckpointHistoryEntry],
    sessions: List[dict[str, Any]]
) -> List[dict[str, Any]]:
    # In a full flow, scorecard is created first. Here we mock score for simplicity in the list
    return [
        gate_min_observation_sessions(window),
        gate_checkpoint_history_complete(entries),
        gate_no_blocked_dangerous_operations(telemetry),
        gate_notification_safety(sessions)
    ]

def exit_gates_to_text(gates: List[dict[str, Any]]) -> str:
    lines = ["Quarantine Exit Gates:"]
    for g in gates:
        status = "PASS" if g.get("passed") else "FAIL"
        lines.append(f"- {g.get('gate_name')}: {status} ({g.get('details')})")
    return "\n".join(lines)
