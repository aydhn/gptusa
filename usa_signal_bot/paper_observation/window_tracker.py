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
    return f"Window Tracker: {window.window_id} ({window.status})\nObserved: {window.observed_session_count}/{window.required_session_count}\nCompleted: {comp}"
