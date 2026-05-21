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
