from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, CheckpointHistoryEntry, ObservationTelemetrySummary, ObservationReview
from usa_signal_bot.paper_observation.window_planner import build_observation_window
from usa_signal_bot.paper_observation.checkpoint_history import build_checkpoint_history
from usa_signal_bot.paper_observation.telemetry_history import aggregate_bridge_telemetry_history
from usa_signal_bot.paper_observation.observation_report import build_observation_review

def observation_window_from_dry_run_bridge_review(payload: dict[str, Any]) -> ObservationWindow:
    return build_observation_window(dry_run_payload=payload)

def checkpoint_history_from_dry_run_bridge_review(payload: dict[str, Any]) -> List[CheckpointHistoryEntry]:
    checkpoints = payload.get("checkpoints", [])
    return build_checkpoint_history(checkpoints)

def telemetry_summary_from_dry_run_bridge_review(payload: dict[str, Any]) -> ObservationTelemetrySummary:
    events = payload.get("telemetry_events", [])
    return aggregate_bridge_telemetry_history(events)

def observation_review_from_dry_run_bridge_review(payload: dict[str, Any]) -> ObservationReview:
    window = observation_window_from_dry_run_bridge_review(payload)
    return build_observation_review(window, dry_run_payload=payload)

def attach_observation_metadata_to_dry_run_payload(payload: dict[str, Any], review: ObservationReview) -> dict[str, Any]:
    payload["observation_metadata"] = {
        "review_id": review.review_id,
        "window_id": review.windows[0].window_id if review.windows else None
    }
    return payload

def dry_run_bridge_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Dry Run Bridge Adapter Info"
