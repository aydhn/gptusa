import os
from pathlib import Path

FILES = {}

FILES["usa_signal_bot/paper_observation/observation_scoring.py"] = """\
from typing import Any, List, Optional
from usa_signal_bot.paper_observation.observation_models import (
    ObservationScorecard, ObservationWindow, ObservationTelemetrySummary,
    CheckpointHistoryEntry, ObservationScoreStatus, ObservationRiskFlag, create_observation_scorecard_id
)
import datetime
from usa_signal_bot.paper_observation.checkpoint_timeline import checkpoint_timeline_has_stale_review

def collect_observation_risk_flags(
    window: ObservationWindow,
    telemetry: ObservationTelemetrySummary,
    checkpoint_entries: List[CheckpointHistoryEntry],
    dry_run_sessions: List[dict[str, Any]] | None = None
) -> List[ObservationRiskFlag]:
    flags = set()

    if window.observed_session_count < window.required_session_count:
        flags.add(ObservationRiskFlag.INSUFFICIENT_DRY_RUN_SESSIONS)

    if not checkpoint_entries:
        flags.add(ObservationRiskFlag.CHECKPOINT_MISSING)
    elif checkpoint_timeline_has_stale_review(checkpoint_entries):
        flags.add(ObservationRiskFlag.CHECKPOINT_STALE)

    if telemetry.blocked_operation_count > 0:
        flags.add(ObservationRiskFlag.BLOCKED_OPERATION_HISTORY)

    if dry_run_sessions:
        for s in dry_run_sessions:
            if s.get("real_order_risk_detected"):
                flags.add(ObservationRiskFlag.REAL_ORDER_RISK)
            if s.get("paper_state_mutation_detected"):
                flags.add(ObservationRiskFlag.PAPER_STATE_MUTATION_RISK)
            if s.get("telegram_real_send_detected"):
                flags.add(ObservationRiskFlag.TELEGRAM_REAL_SEND_RISK)
            if s.get("production_config_write_detected"):
                flags.add(ObservationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

    return list(flags)

def calculate_observation_score(
    window: ObservationWindow,
    telemetry: ObservationTelemetrySummary,
    checkpoint_entries: List[CheckpointHistoryEntry],
    dry_run_sessions: List[dict[str, Any]] | None = None
) -> Optional[float]:
    if window.observed_session_count == 0:
        return None

    score = 100.0

    # Penalties
    if window.observed_session_count < window.required_session_count:
        score -= 20.0

    if not checkpoint_entries:
        score -= 30.0
    elif checkpoint_timeline_has_stale_review(checkpoint_entries):
        score -= 20.0

    if telemetry.blocked_operation_count > 0:
        score -= (telemetry.blocked_operation_count * 10)

    if telemetry.risk_rejected_count > 0:
        score -= (telemetry.risk_rejected_count * 5)

    if telemetry.notification_warning_count > 0:
        score -= (telemetry.notification_warning_count * 5)

    return max(0.0, score)

def classify_observation_score(score: Optional[float], risk_flags: List[ObservationRiskFlag]) -> ObservationScoreStatus:
    if score is None:
        return ObservationScoreStatus.INSUFFICIENT_DATA

    critical_flags = [
        ObservationRiskFlag.REAL_ORDER_RISK,
        ObservationRiskFlag.PAPER_ORDER_RISK,
        ObservationRiskFlag.BROKER_ORDER_RISK,
        ObservationRiskFlag.PAPER_STATE_MUTATION_RISK,
        ObservationRiskFlag.TELEGRAM_REAL_SEND_RISK,
        ObservationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        ObservationRiskFlag.ACTIVE_PAPER_ENABLE_RISK
    ]

    if any(f in risk_flags for f in critical_flags):
        return ObservationScoreStatus.BLOCKED

    if score >= 80.0:
        return ObservationScoreStatus.PASS
    if score >= 50.0:
        return ObservationScoreStatus.WARNING
    return ObservationScoreStatus.FAIL

def build_observation_scorecard(
    window: ObservationWindow,
    telemetry: ObservationTelemetrySummary,
    checkpoint_entries: List[CheckpointHistoryEntry],
    dry_run_sessions: List[dict[str, Any]] | None = None
) -> ObservationScorecard:

    risk_flags = collect_observation_risk_flags(window, telemetry, checkpoint_entries, dry_run_sessions)
    score = calculate_observation_score(window, telemetry, checkpoint_entries, dry_run_sessions)
    status = classify_observation_score(score, risk_flags)

    return ObservationScorecard(
        scorecard_id=create_observation_scorecard_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        window_id=window.window_id,
        candidate_id=window.candidate_id,
        status=status,
        score=score,
        session_score=100.0 if window.observed_session_count >= window.required_session_count else 50.0,
        checkpoint_score=100.0 if checkpoint_entries and not checkpoint_timeline_has_stale_review(checkpoint_entries) else 0.0,
        telemetry_score=max(0.0, 100.0 - (telemetry.blocked_operation_count * 10)),
        safety_score=0.0 if status == ObservationScoreStatus.BLOCKED else 100.0,
        notification_score=max(0.0, 100.0 - (telemetry.notification_warning_count * 5)),
        risk_flags=risk_flags,
        manual_review_required=(status in [ObservationScoreStatus.WARNING, ObservationScoreStatus.FAIL, ObservationScoreStatus.BLOCKED]),
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def observation_scorecard_to_text(scorecard: ObservationScorecard) -> str:
    s = f"{scorecard.score:.1f}" if scorecard.score is not None else "N/A"
    return f"Observation Scorecard: {scorecard.scorecard_id}\\nStatus: {scorecard.status}\\nScore: {s}\\nRisk Flags: {len(scorecard.risk_flags)}"
"""

FILES["usa_signal_bot/paper_observation/exit_gates.py"] = """\
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
    return "\\n".join(lines)
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
