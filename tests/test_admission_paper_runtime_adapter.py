from usa_signal_bot.paper_admission_review.paper_runtime_adapter import build_read_only_paper_snapshot_for_admission_review, validate_paper_runtime_not_mutated_by_admission_review

def test_build_read_only_paper_snapshot():
    payload = {"state": "active"}
    snapshot = build_read_only_paper_snapshot_for_admission_review(payload)
    assert snapshot["readonly"]
    assert snapshot["state"] == "active"

def test_validate_paper_runtime_not_mutated():
    errors = validate_paper_runtime_not_mutated_by_admission_review({}, {"paper_state_committed": True})
    assert len(errors) > 0

    errors = validate_paper_runtime_not_mutated_by_admission_review({}, {"paper_state_committed": False})
    assert len(errors) == 0
