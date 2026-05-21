import os
from pathlib import Path

FILES = {}

FILES["usa_signal_bot/paper_observation/window_planner.py"] = """\
from typing import Any, Optional, List
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationWindowStatus, ObservationWindowMode, create_observation_window_id
import datetime

def observation_window_end_at(days: int = 7) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    end_date = now + datetime.timedelta(days=days)
    return end_date.isoformat()

def build_observation_window(candidate_payload: dict[str, Any] | None = None, dry_run_payload: dict[str, Any] | None = None, required_session_count: int = 3, window_days: int = 7) -> ObservationWindow:
    cand_id = candidate_payload.get("candidate_id") if candidate_payload else None
    tick_id = candidate_payload.get("ticket_id") if candidate_payload else None

    # If using Python 3.10+, datetime.datetime.now(datetime.UTC) is preferred, but timezone.utc is safe
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    end_utc = observation_window_end_at(window_days)

    dry_run_ids = dry_run_payload.get("session_ids", []) if dry_run_payload else []

    return ObservationWindow(
        window_id=create_observation_window_id(),
        created_at_utc=now_utc,
        candidate_id=cand_id,
        ticket_id=tick_id,
        status=ObservationWindowStatus.PLANNED,
        mode=ObservationWindowMode.FULL_SUPERVISED_OBSERVATION,
        started_at_utc=None,
        ends_at_utc=end_utc,
        required_session_count=max(1, required_session_count),
        observed_session_count=0,
        dry_run_session_ids=dry_run_ids,
        checkpoint_ids=[],
        telemetry_event_count=0,
        blocked_operation_count=0,
        manual_review_required=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def default_observation_window(candidate_id: str | None = None, ticket_id: str | None = None) -> ObservationWindow:
    return build_observation_window(
        candidate_payload={"candidate_id": candidate_id, "ticket_id": ticket_id}
    )

def validate_observation_window_plan(window: ObservationWindow) -> List[str]:
    errors = []
    if window.allows_active_paper or window.allows_broker_execution or window.allows_paper_state_mutation or window.allows_config_patch:
        errors.append("Window plan allows forbidden active execution flags.")
    if window.required_session_count <= 0:
        errors.append("required_session_count must be positive.")
    return errors

def observation_window_plan_summary(window: ObservationWindow) -> dict[str, Any]:
    return {
        "window_id": window.window_id,
        "status": window.status,
        "candidate_id": window.candidate_id,
        "required_sessions": window.required_session_count
    }

def observation_window_plan_to_text(window: ObservationWindow) -> str:
    return f"Observation Window Plan: {window.window_id} ({window.status})\\nCandidate: {window.candidate_id}\\nRequired Sessions: {window.required_session_count}"
"""

FILES["usa_signal_bot/paper_observation/window_tracker.py"] = """\
from typing import Any
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationWindowStatus
import datetime

def update_observation_window_with_session(window: ObservationWindow, session_payload: dict[str, Any]) -> ObservationWindow:
    session_id = session_payload.get("session_id")
    if session_id and session_id not in window.dry_run_session_ids:
        window.dry_run_session_ids.append(session_id)
        window.observed_session_count += 1

    if window.status == ObservationWindowStatus.PLANNED:
        window.status = ObservationWindowStatus.ACTIVE_METADATA_ONLY
        window.started_at_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    return window

def update_observation_window_with_checkpoint(window: ObservationWindow, checkpoint_payload: dict[str, Any]) -> ObservationWindow:
    cp_id = checkpoint_payload.get("checkpoint_id")
    if cp_id and cp_id not in window.checkpoint_ids:
        window.checkpoint_ids.append(cp_id)
    return window

def observation_window_completed(window: ObservationWindow) -> bool:
    return window.observed_session_count >= window.required_session_count

def observation_window_expired(window: ObservationWindow, now_utc: str | None = None) -> bool:
    if not window.ends_at_utc:
        return False
    now = now_utc or datetime.datetime.now(datetime.timezone.utc).isoformat()
    return now > window.ends_at_utc

def observation_window_blocked(window: ObservationWindow) -> bool:
    return window.status in [ObservationWindowStatus.BLOCKED, ObservationWindowStatus.REJECTED]

def observation_window_tracker_summary(window: ObservationWindow) -> dict[str, Any]:
    return {
        "window_id": window.window_id,
        "status": window.status,
        "observed_sessions": window.observed_session_count,
        "completed": observation_window_completed(window),
        "expired": observation_window_expired(window)
    }

def observation_window_tracker_to_text(window: ObservationWindow) -> str:
    comp = "Yes" if observation_window_completed(window) else "No"
    return f"Window Tracker: {window.window_id} ({window.status})\\nObserved: {window.observed_session_count}/{window.required_session_count}\\nCompleted: {comp}"
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
