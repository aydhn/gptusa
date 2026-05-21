from typing import Any
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, QuarantineExitReview, ObservationReview
from usa_signal_bot.paper_observation.window_planner import build_observation_window
from usa_signal_bot.paper_observation.observation_report import build_quarantine_exit_review
from usa_signal_bot.paper_observation.telemetry_history import aggregate_bridge_telemetry_history

def observation_window_from_quarantine_review(payload: dict[str, Any]) -> ObservationWindow:
    return build_observation_window(candidate_payload=payload)

def quarantine_exit_review_from_quarantine_payload(payload: dict[str, Any], dry_run_payload: dict[str, Any] | None = None) -> QuarantineExitReview:
    window = observation_window_from_quarantine_review(payload)
    events = dry_run_payload.get("telemetry_events", []) if dry_run_payload else []
    telemetry = aggregate_bridge_telemetry_history(events)
    return build_quarantine_exit_review(window, telemetry, [])

def attach_observation_review_to_quarantine_payload(payload: dict[str, Any], review: ObservationReview) -> dict[str, Any]:
    payload["observation_review_id"] = review.review_id
    return payload

def paper_quarantine_observation_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"quarantine_status": payload.get("status")}

def paper_quarantine_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Paper Quarantine Adapter Info"
