import os
from pathlib import Path

FILES = {}

FILES["tests/test_observation_dry_run_bridge_adapter.py"] = """\
from usa_signal_bot.paper_observation.dry_run_bridge_adapter import (
    observation_window_from_dry_run_bridge_review, checkpoint_history_from_dry_run_bridge_review,
    telemetry_summary_from_dry_run_bridge_review, observation_review_from_dry_run_bridge_review,
    attach_observation_metadata_to_dry_run_payload, dry_run_bridge_adapter_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_dry_run_bridge_adapter():
    payload = {
        "session_ids": ["s1"],
        "checkpoints": [{"checkpoint_id": "cp1", "status": "REVIEWED"}],
        "telemetry_events": [{"event_type": "PROPOSAL"}]
    }

    win = observation_window_from_dry_run_bridge_review(payload)
    assert "s1" in win.dry_run_session_ids

    hist = checkpoint_history_from_dry_run_bridge_review(payload)
    assert hist[0].checkpoint_id == "cp1"

    tel = telemetry_summary_from_dry_run_bridge_review(payload)
    assert tel.proposal_count == 1

    rev = observation_review_from_dry_run_bridge_review(payload)
    assert len(rev.windows) == 1

    pl = attach_observation_metadata_to_dry_run_payload({}, rev)
    assert "observation_metadata" in pl

    text = dry_run_bridge_adapter_to_text(payload)
    assert "Adapter Info" in text
"""

FILES["tests/test_observation_paper_quarantine_adapter.py"] = """\
from usa_signal_bot.paper_observation.paper_quarantine_adapter import (
    observation_window_from_quarantine_review, quarantine_exit_review_from_quarantine_payload,
    attach_observation_review_to_quarantine_payload, paper_quarantine_observation_summary,
    paper_quarantine_adapter_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_paper_quarantine_adapter():
    payload = {"candidate_id": "c1", "status": "ENROLLED"}
    win = observation_window_from_quarantine_review(payload)
    assert win.candidate_id == "c1"

    exit_rev = quarantine_exit_review_from_quarantine_payload(payload, {"telemetry_events": []})
    assert exit_rev.candidate_id == "c1"

    rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [], [], [], [], [], [], {})
    pl = attach_observation_review_to_quarantine_payload(payload.copy(), rev)
    assert pl["observation_review_id"] == "r1"

    summ = paper_quarantine_observation_summary(payload)
    assert summ["quarantine_status"] == "ENROLLED"

    text = paper_quarantine_adapter_to_text(payload)
    assert "Adapter Info" in text
"""

FILES["tests/test_observation_shadow_governance_adapter.py"] = """\
from usa_signal_bot.paper_observation.shadow_governance_adapter import (
    observation_requirements_from_shadow_governance, shadow_governance_supports_observation,
    attach_observation_hint_to_shadow_governance, shadow_governance_observation_summary,
    shadow_governance_adapter_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_shadow_governance_adapter():
    req = observation_requirements_from_shadow_governance({})
    assert req["required_sessions"] == 3

    sup, _ = shadow_governance_supports_observation({})
    assert sup is True

    rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [], [], [], [], [], [], {})
    pl = attach_observation_hint_to_shadow_governance({}, rev)
    assert "observation_hint" in pl

    summ = shadow_governance_observation_summary({})
    assert summ["shadow_governance"] == "Attached"

    text = shadow_governance_adapter_to_text({})
    assert "Adapter Info" in text
"""

FILES["tests/test_observation_paper_runtime_adapter.py"] = """\
from usa_signal_bot.paper_observation.paper_runtime_adapter import (
    build_read_only_paper_observation_snapshot, compare_observation_to_paper_snapshot,
    validate_paper_snapshot_not_mutated_for_observation, attach_observation_metadata_to_paper_analytics,
    paper_runtime_observation_adapter_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_paper_runtime_adapter():
    snap = build_read_only_paper_observation_snapshot()
    assert snap["read_only"] is True
    assert snap["paper_state_committed"] is False

    rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [], [], [], [], [], [], {})
    comp = compare_observation_to_paper_snapshot(rev, snap)
    assert "diff" in comp

    errors = validate_paper_snapshot_not_mutated_for_observation(snap, {"paper_state_committed": True})
    assert len(errors) == 1

    pl = attach_observation_metadata_to_paper_analytics({}, rev)
    assert "observation_metadata" in pl

    text = paper_runtime_observation_adapter_to_text({})
    assert "Adapter Info" in text
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
