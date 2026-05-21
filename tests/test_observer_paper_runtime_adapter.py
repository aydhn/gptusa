from usa_signal_bot.paper_observer.paper_runtime_adapter import (
    build_read_only_paper_runtime_snapshot_for_observer,
    compare_observer_outputs_to_paper_snapshot,
    validate_paper_runtime_not_mutated_by_observer,
    attach_observer_metadata_to_paper_analytics
)
from usa_signal_bot.paper_observer.observer_report import build_paper_observer_review
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment

def test_paper_runtime_adapter():
    snapshot = build_read_only_paper_runtime_snapshot_for_observer({"key": "value"})
    assert snapshot["key"] == "value"

    comp = compare_observer_outputs_to_paper_snapshot([], snapshot)
    assert "drifts_detected" in comp

    errors = validate_paper_runtime_not_mutated_by_observer({"a": 1}, {"a": 1})
    assert len(errors) == 0

    errors = validate_paper_runtime_not_mutated_by_observer({"a": 1}, {"a": 2})
    assert len(errors) == 1

    enrollment = build_observer_enrollment("cand_1", "t1", "OK")
    review = build_paper_observer_review(enrollment)
    payload = attach_observer_metadata_to_paper_analytics({}, review)
    assert "paper_observer_analytics" in payload
