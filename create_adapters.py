import os
from pathlib import Path

FILES = {}

FILES["usa_signal_bot/paper_observation/dry_run_bridge_adapter.py"] = """\
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
"""

FILES["usa_signal_bot/paper_observation/paper_quarantine_adapter.py"] = """\
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
"""

FILES["usa_signal_bot/paper_observation/shadow_governance_adapter.py"] = """\
from typing import Any, Tuple, List
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def observation_requirements_from_shadow_governance(payload: dict[str, Any]) -> dict[str, Any]:
    return {"required_sessions": 3}

def shadow_governance_supports_observation(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_observation_hint_to_shadow_governance(payload: dict[str, Any], review: ObservationReview) -> dict[str, Any]:
    payload["observation_hint"] = "Review completed"
    return payload

def shadow_governance_observation_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"shadow_governance": "Attached"}

def shadow_governance_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Shadow Governance Adapter Info"
"""

FILES["usa_signal_bot/paper_observation/paper_runtime_adapter.py"] = """\
from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def build_read_only_paper_observation_snapshot(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "read_only": True,
        "paper_state_committed": False,
        "paper_order_executed": False,
        "portfolio_state_mutated": False
    }

def compare_observation_to_paper_snapshot(review: ObservationReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"diff": "No real difference, paper is read only."}

def validate_paper_snapshot_not_mutated_for_observation(before: dict[str, Any], after: dict[str, Any]) -> List[str]:
    errors = []
    if after.get("paper_state_committed"):
        errors.append("paper_state_committed is True")
    if after.get("paper_order_executed"):
        errors.append("paper_order_executed is True")
    if after.get("portfolio_state_mutated"):
        errors.append("portfolio_state_mutated is True")
    return errors

def attach_observation_metadata_to_paper_analytics(payload: dict[str, Any], review: ObservationReview) -> dict[str, Any]:
    payload["observation_metadata"] = {"review_id": review.review_id}
    return payload

def paper_runtime_observation_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Paper Runtime Adapter Info"
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
