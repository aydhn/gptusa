import os
from pathlib import Path

FILES = {}

FILES["tests/test_observation_dry_run_ingestion.py"] = """\
from usa_signal_bot.paper_observation.dry_run_ingestion import (
    ingest_dry_run_bridge_review, extract_dry_run_sessions, extract_dry_run_session_ids,
    extract_human_checkpoints, extract_bridge_telemetry_events, dry_run_ingestion_warnings, dry_run_ingestion_to_text
)

def test_dry_run_ingestion():
    payload = {
        "sessions": [{"session_id": "s1"}],
        "checkpoints": [{"checkpoint_id": "cp1"}],
        "telemetry_events": [{"event_type": "BLOCKED_OPERATION"}],
        "blocked_operation_count": 1
    }

    res = ingest_dry_run_bridge_review(payload)
    assert len(extract_dry_run_sessions(res)) == 1
    assert "s1" in extract_dry_run_session_ids(res)
    assert len(extract_human_checkpoints(res)) == 1
    assert len(extract_bridge_telemetry_events(res)) == 1

    warnings = dry_run_ingestion_warnings(res)
    assert any("Blocked operations" in w for w in warnings)

    text = dry_run_ingestion_to_text(res)
    assert "Dry-run Bridge Review" in text
"""

FILES["tests/test_observation_quarantine_ingestion.py"] = """\
from usa_signal_bot.paper_observation.quarantine_ingestion import (
    ingest_quarantine_payload, extract_candidate_id_from_quarantine, extract_ticket_id_from_quarantine,
    extract_quarantine_status, quarantine_payload_supports_observation, quarantine_ingestion_to_text
)

def test_quarantine_ingestion():
    payload = {
        "candidate_id": "c1",
        "ticket_id": "t1",
        "status": "ENROLLED"
    }
    res = ingest_quarantine_payload(payload)
    assert extract_candidate_id_from_quarantine(res) == "c1"
    assert extract_ticket_id_from_quarantine(res) == "t1"
    assert extract_quarantine_status(res) == "ENROLLED"

    supports, _ = quarantine_payload_supports_observation(res)
    assert supports is True

    text = quarantine_ingestion_to_text(res)
    assert "c1" in text

    payload_blocked = {"status": "BLOCKED"}
    supports, _ = quarantine_payload_supports_observation(payload_blocked)
    assert supports is False
"""

FILES["tests/test_observation_window_planner.py"] = """\
from usa_signal_bot.paper_observation.window_planner import build_observation_window, default_observation_window, observation_window_end_at, validate_observation_window_plan, observation_window_plan_summary, observation_window_plan_to_text

def test_window_planner():
    window = build_observation_window({"candidate_id": "c1", "ticket_id": "t1"}, None, 3, 7)
    assert window.candidate_id == "c1"
    assert window.ticket_id == "t1"
    assert window.required_session_count == 3
    assert window.allows_active_paper is False

    def_win = default_observation_window("c2", "t2")
    assert def_win.candidate_id == "c2"

    end_dt = observation_window_end_at(7)
    assert end_dt is not None

    errors = validate_observation_window_plan(window)
    assert len(errors) == 0

    summary = observation_window_plan_summary(window)
    assert summary["candidate_id"] == "c1"

    text = observation_window_plan_to_text(window)
    assert "c1" in text
"""

FILES["tests/test_observation_window_tracker.py"] = """\
from usa_signal_bot.paper_observation.window_planner import default_observation_window
from usa_signal_bot.paper_observation.window_tracker import (
    update_observation_window_with_session, update_observation_window_with_checkpoint,
    observation_window_completed, observation_window_expired, observation_window_blocked,
    observation_window_tracker_summary, observation_window_tracker_to_text
)
import datetime

def test_window_tracker():
    window = default_observation_window("c1", "t1")
    window.required_session_count = 1

    assert observation_window_completed(window) is False

    window = update_observation_window_with_session(window, {"session_id": "s1"})
    assert "s1" in window.dry_run_session_ids
    assert observation_window_completed(window) is True

    window = update_observation_window_with_checkpoint(window, {"checkpoint_id": "cp1"})
    assert "cp1" in window.checkpoint_ids

    assert observation_window_blocked(window) is False

    now = datetime.datetime.now(datetime.timezone.utc)
    future = (now + datetime.timedelta(days=10)).isoformat()
    assert observation_window_expired(window, future) is True

    summary = observation_window_tracker_summary(window)
    assert summary["completed"] is True

    text = observation_window_tracker_to_text(window)
    assert "Yes" in text
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
