from usa_signal_bot.paper_observation.checkpoint_history import build_checkpoint_history
from usa_signal_bot.paper_observation.checkpoint_timeline import (
    sort_checkpoint_history, latest_checkpoint, checkpoint_timeline_has_stale_review,
    checkpoint_timeline_required_followups, checkpoint_timeline_summary, checkpoint_timeline_to_text
)

def test_checkpoint_timeline():
    history = build_checkpoint_history([
        {"checkpoint_id": "cp1", "status": "REVIEWED"},
        {"checkpoint_id": "cp2", "status": "WAITING_REVIEW"}
    ])

    # modify dates slightly
    history[0].created_at_utc = "2023-01-01T00:00:00Z"
    history[1].created_at_utc = "2023-01-02T00:00:00Z"

    sorted_h = sort_checkpoint_history(history)
    assert sorted_h[0].checkpoint_id == "cp1"

    latest = latest_checkpoint(history)
    assert latest is not None
    assert latest.checkpoint_id == "cp2"

    # Since dates are old, it should be stale
    assert checkpoint_timeline_has_stale_review(history) is True

    followups = checkpoint_timeline_required_followups(history)
    assert len(followups) > 0

    summary = checkpoint_timeline_summary(history)
    assert summary["is_stale"] is True

    text = checkpoint_timeline_to_text(history)
    assert "Yes" in text
