from usa_signal_bot.paper_observation.checkpoint_history import (
    build_checkpoint_history_entry, build_checkpoint_history, checkpoint_history_status,
    checkpoint_history_warnings, checkpoint_history_summary, checkpoint_history_to_text
)
from usa_signal_bot.core.enums import CheckpointHistoryStatus

def test_checkpoint_history():
    c1 = {"checkpoint_id": "cp1", "status": "REVIEWED"}
    c2 = {"checkpoint_id": "cp2", "status": "WAITING_REVIEW"}

    entry = build_checkpoint_history_entry(c1)
    assert entry.checkpoint_id == "cp1"
    assert entry.allows_active_paper is False

    history = build_checkpoint_history([c1, c2])
    assert len(history) == 2

    assert checkpoint_history_status([]) == CheckpointHistoryStatus.EMPTY
    assert checkpoint_history_status(history) == CheckpointHistoryStatus.PARTIAL

    complete_history = build_checkpoint_history([c1, {"checkpoint_id": "cp3", "status": "APPROVED"}])
    assert checkpoint_history_status(complete_history) == CheckpointHistoryStatus.COMPLETE

    warnings = checkpoint_history_warnings(history)
    assert any("waiting for review" in w for w in warnings)

    summary = checkpoint_history_summary(history)
    assert summary["waiting_review_count"] == 1

    text = checkpoint_history_to_text(history)
    assert "PARTIAL" in text
